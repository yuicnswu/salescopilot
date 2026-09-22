# ⚡ WARRIX Live Commerce Studio Hub (100 SKUs)

ระบบคลังข้อมูลสินค้าและสคริปต์ช่วยขายหน้ากล้อง (RAG & Interactive Studio) แบรนด์ **WARRIX** รวม 100 รายการสินค้า ครบทุกหมวดหมู่ พร้อมรูปภาพ ลิงก์ตรงหน้าเว็บและ Shopee

🌐 **Live Demo (GitHub Pages):** `https://<YOUR-GITHUB-USERNAME>.github.io/<REPO-NAME>/`

---

## 🌟 จุดเด่นของระบบ (Key Features)

1. **🎙️ Live Prompter Mode:** การ์ดสปีชพูดสดหน้ากล้องสำหรับ MC (Hook ดึงดูด, Pain Point จี้ใจ, Live Demo สาธิตสินค้า, Interactive CTA กระตุ้นปิดการขาย, Basket Builder แนะนำสินค้าคู่)
2. **📱 Grid Catalog Mode:** แคตตาล็อกสินค้า 100 SKUs พร้อมภาพตัวอย่าง ขนาด และช่วงราคา
3. **📊 Price Matrix Mode:** ตารางเปรียบเทียบราคาหน้าเว็บ (MSRP) กับราคาโปรโมชันสดในไลฟ์ พร้อมคำนวณ % ส่วนลด
4. **🔍 Real-Time Fuzzy Search:** ค้นหาตามรหัส SKU, ชื่อสินค้า, เนื้อผ้า, ทรงเสื้อ หรือคำโปรย
5. **🏷️ Category Filtering:** ฟิลเตอร์ด่วนแยกตามหมวดหมู่ (Polo, ทีมชาติไทย, รองเท้า, แจ็คเก็ต, กระเป๋า, วิ่ง ฯลฯ)
6. **🔗 Verified Direct Links:** ลิงก์ตรงไปยังสินค้าบน [Warrix.com](https://www.warrix.com) และ [Shopee Warrix Official Store](https://shopee.co.th/warrix.official)

---

## 🚀 วิธีการเปิดใช้งานบน GitHub Pages

### ขั้นตอนที่ 1: Push โค้ดขึ้น GitHub Repository
```bash
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/<REPO-NAME>.git
git branch -M main
git push -u origin main
```

### ขั้นตอนที่ 2: เปิดใช้งาน GitHub Pages
1. เข้าไปที่หน้า Repository ของคุณบน GitHub
2. คลิกแถบ **Settings** (การตั้งค่า)
3. เลือกเมนู **Pages** ที่แถบเมนูด้านซ้าย
4. ในส่วน **Build and deployment > Source**:
   * เลือก **Deploy from a branch**
   * Branch: เลือก `main` และโฟลเดอร์ `/ (root)`
   * กด **Save**
5. รอระบบ GitHub Build ประมาณ 1-2 นาที คุณจะได้ URL สำหรับเปิดใช้งานทันที เช่น:
   `https://<YOUR-GITHUB-USERNAME>.github.io/<REPO-NAME>/`
