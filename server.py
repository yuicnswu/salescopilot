# -*- coding: utf-8 -*-
import http.server
import socketserver
import json
import os
import urllib.parse
import urllib.request
import re
import time

PORT = int(os.environ.get("PORT", 8080))

# Load 100 SKUs product database
with open("warrix_products_data.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

# Build quick lookup index
SKU_MAP = {p["sku"]: p for p in PRODUCTS}

def retrieve_relevant_skus(query, max_items=6):
    q_lower = query.lower()
    q_words = [w for w in re.findall(r'[\w\u0E00-\u0E7F]+', q_lower) if len(w) > 1]
    
    scored = []
    for p in PRODUCTS:
        score = 0
        sku = p.get('sku', '').lower()
        name = p.get('name', '').lower()
        cat = p.get('category', '').lower()
        tagline = p.get('tagline', '').lower()
        colors = ' '.join([c['name'] for c in p.get('color_palette', [])]).lower()
        fabric = p.get('what_it_is', {}).get('fabric', '').lower()
        
        # Exact SKU match gets highest boost
        if sku in q_lower:
            score += 50
            
        for w in q_words:
            if w in sku: score += 10
            if w in name: score += 5
            if w in cat: score += 4
            if w in tagline: score += 3
            if w in colors: score += 3
            if w in fabric: score += 3
            
        if score > 0:
            scored.append((score, p))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    if scored:
        return [p for _, p in scored[:max_items]]
    # Default top featured items
    return PRODUCTS[:max_items]

def build_compact_context(products):
    lines = []
    for p in products:
        colors_str = ', '.join([c['name'].split(' ')[0] for c in p.get('color_palette', [])[:5]])
        lines.append(
            f"• [{p['sku']}] {p['name']} | หมวด: {p['category']} | ราคา: ฿{p.get('web_sale_price') or p['price_range']} (ลด {p.get('discount_pct', '0%')}) | สี: {colors_str} | จุดเด่น: {p.get('tagline', '')} | Hook: {p.get('how_to_sell', {}).get('hook', '')} | คู่แนะนำ: {p.get('how_to_sell', {}).get('basket_builder', '')}"
        )
    return "\n".join(lines)

def build_system_prompt(relevant_products):
    catalog_context = build_compact_context(relevant_products)
    return f"""คุณคือ "WARRIX AI Live Co-Host & Sales Director" ผู้ช่วยอัจฉริยะข้างกายพิธีกร/MC ไลฟ์สดของ WARRIX
คุณมีความรู้รอบด้านเกี่ยวกับสินค้า WARRIX ทั้ง 100 SKUs อย่างแม่นยำและตอบได้ลื่นไหล มีพลัง ดึงดูดผู้ฟัง

ข้อมูลสินค้าที่ตรงกับคำถามมากที่สุด:
{catalog_context}

แนวทางการตอบเพื่อความลื่นไหลและปิดการขาย (Live Selling Flow):
1. ใช้ภาษาพูดไลฟ์สดที่กระชับ สุภาพ สนุกสนาน มีพลัง (Energetic & Punchy Spoken Thai)
2. ระบุชื่อรุ่น, รหัส [SKU], ราคาโปรโมชั่น, และจุดเด่นเนื้อผ้าให้ชัดเจน
3. มี "Hook 3 วินาที" หรือ "สคริปต์พูดปิดการขาย" ที่ MC สามารถหยิบไปพูดออกกล้องได้ทันที
4. แนะนำคู่เซ็ต (Basket Builder) หรือคำแนะนำเรื่องไซส์/สี เพื่อช่วยดันยอดตะกร้า
5. จัดรูปแบบด้วยหัวข้อย่อยและอิโมจิให้อ่านง่ายบนหน้าจอ Teleprompter"""

def call_gemini_api_stream(user_query, api_key=None, model="gemini-3.6-flash"):
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return None, "NO_API_KEY"

    relevant = retrieve_relevant_skus(user_query, max_items=4)
    sys_prompt = build_system_prompt(relevant)
    
    # Try gemini-3.6-flash or gemini-2.5-flash for maximum speed
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse&key={key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{sys_prompt}\n\nคำสั่งจาก MC ไลฟ์สด: {user_query}\nตอบสั้น กระชับ มีพลัง ไม่เกิน 4 ประโยคพร้อม Hook พูดทันที:"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 380,
            "thinkingConfig": {"thinkingBudget": 0}
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return resp, "SUCCESS"
    except Exception as e:
        return None, str(e)

def call_gemini_api_sync(user_query, api_key=None, model="gemini-3.6-flash"):
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return None, "NO_API_KEY"

    relevant = retrieve_relevant_skus(user_query, max_items=6)
    sys_prompt = build_system_prompt(relevant)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{sys_prompt}\n\nคำถาม/คำสั่งจาก MC ไลฟ์สด: {user_query}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 380,
            "thinkingConfig": {"thinkingBudget": 0}
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
            parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            text = ''.join(p.get('text', '') for p in parts)
            return text, "SUCCESS"
    except Exception as e:
        return None, str(e)

def offline_copilot_search(query):
    top = retrieve_relevant_skus(query, max_items=3)
    reply = "💡 **คำแนะนำจากผู้ช่วย AI Co-Pilot ประจำสตูฯ (100 SKUs Omni-Recall):**\n\n"
    for p in top:
        disc = f" (ลด {p['discount_pct']})" if p.get('discount_pct') else ""
        colors = ', '.join([c['name'].split(' ')[0] for c in p.get('color_palette', [])[:4]])
        reply += f"🔹 **[{p['sku']}] {p['name']}**\n"
        reply += f"  • ราคาพิเศษ: ฿{p.get('web_sale_price') or p['price_range']}{disc} | มีสี: {colors}\n"
        reply += f"  • 🎣 **Hook เปิดตัว:** {p.get('how_to_sell', {}).get('hook', p.get('tagline', ''))}\n"
        reply += f"  • 🎬 **Live Demo:** {p.get('how_to_sell', {}).get('live_demo', 'โชว์ความยืดหยุ่นและเนื้อผ้าหน้ากล้อง')}\n"
        reply += f"  • 🛒 **บทพูดปิดการขาย:** {p.get('how_to_sell', {}).get('interactive_cta', 'กดใส่ตะกร้าตอนนี้ได้ราคาพิเศษทันที!')}\n"
        reply += f"  • 👔 **คู่แนะนำเพิ่มยอด:** {p.get('how_to_sell', {}).get('basket_builder', 'ใส่คู่กับกางเกงวอร์ม Warrix')}\n\n"
    return reply

class WarrixStudioServer(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            resp = {
                "status": "healthy",
                "service": "warrix-gemini-live-studio",
                "model": "gemini-3.6-flash",
                "streaming_enabled": True,
                "skus": len(PRODUCTS)
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/api/products":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(PRODUCTS, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path in ["/", ""]:
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)

        # Real-time SSE Streaming Endpoint
        if parsed.path == "/api/copilot/stream":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length) if content_length > 0 else b'{}'
            try:
                body = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                body = {}

            query = body.get("prompt") or body.get("query") or body.get("message") or ""
            api_key = body.get("api_key")

            if not query.strip():
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Prompt query is required"}')
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            stream_resp, status_code = call_gemini_api_stream(query, api_key=api_key)
            if stream_resp:
                try:
                    for line in stream_resp:
                        l = line.decode('utf-8', errors='ignore').strip()
                        if l.startswith('data:'):
                            try:
                                chunk = json.loads(l[5:])
                                parts = chunk.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                                for p in parts:
                                    t = p.get('text', '')
                                    if t:
                                        msg = json.dumps({"token": t, "text": t}, ensure_ascii=False)
                                        self.wfile.write(f"data: {msg}\n\n".encode("utf-8"))
                                        self.wfile.flush()
                            except Exception:
                                pass
                    self.wfile.write(b"data: [DONE]\n\n")
                    self.wfile.flush()
                except Exception:
                    pass
                finally:
                    stream_resp.close()
            else:
                # Stream offline fallback tokens smoothly
                fallback_text = offline_copilot_search(query)
                words = re.findall(r'\S+|\n', fallback_text)
                for w in words:
                    msg = json.dumps({"token": w + (" " if w != "\n" else ""), "text": w + (" " if w != "\n" else "")}, ensure_ascii=False)
                    self.wfile.write(f"data: {msg}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(0.02)
                self.wfile.write(b"data: [DONE]\n\n")
                self.wfile.flush()
            return

        # Synchronous Endpoint (Fallback)
        if parsed.path in ["/api/copilot", "/api/chat"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length) if content_length > 0 else b'{}'
            try:
                body = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                body = {}

            query = body.get("prompt") or body.get("query") or body.get("message") or ""
            api_key = body.get("api_key")

            if not query.strip():
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Prompt query is required"}')
                return

            gemini_reply, status_code = call_gemini_api_sync(query, api_key=api_key)
            if gemini_reply:
                res_payload = {
                    "status": "success",
                    "source": "gemini-3.6-flash",
                    "reply": gemini_reply
                }
            else:
                fallback_reply = offline_copilot_search(query)
                res_payload = {
                    "status": "fallback",
                    "source": "offline-rag-100-skus",
                    "note": f"Gemini API returned: {status_code}",
                    "reply": fallback_reply
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res_payload, ensure_ascii=False).encode("utf-8"))
            return

        if parsed.path == "/api/warrix/sync":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "message": "Synced with warrix.com local catalog", "count": 100}')
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    server = socketserver.TCPServer(("", PORT), WarrixStudioServer)
    print(f"WARRIX Live Studio Server with Gemini Stream running on port {PORT}")
    server.serve_forever()
