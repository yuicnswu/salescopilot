# -*- coding: utf-8 -*-
import json

DATA_PATH = '/Users/cattleya.c/.gemini/users/user1/warrix_products_data.json'

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Adding 4-Level Fashion Value Ladder to {len(products)} products...")

def build_value_ladder(p):
    cat = p.get('category', '').strip()
    name = p.get('name', '').strip()
    sku = p.get('sku', '').strip()
    fabric = p.get('product_details', {}).get('fabric', '').strip()
    design = p.get('product_details', {}).get('key_design', '').strip()
    
    # 1. POLO SHIRTS
    if cat == 'Polo Shirts':
        if 'Jacquard' in fabric or 'อะตอม' in fabric:
            attr = "ผ้า Jacquard อะตอมเล่นแสง + ปก Short Collar"
        elif 'Emboss' in fabric or 'ปั๊มนูน' in design:
            attr = "เทคนิค Emboss ลาย 3D + ปก Short Collar"
        elif 'Bubble' in name or 'วาฟเฟิล' in fabric:
            attr = "เนื้อผ้า Bubble Knit ทอสัมผัสนุ่มมีมิติ"
        else:
            attr = "เส้นใย Polyester ระบายอากาศ + ปกทรงโมเดิร์น"
            
        func = "ระบายเหงื่อไว ซักสะบัดตากไม่ต้องรีด ทรงไม่แก่"
        emot = "มั่นใจตลอดวัน ไร้กังวลเรื่องคราบเหงื่อและพุงยื่น"
        ident = "ลุค Young Executive สมาร์ทดูแพงแบบ Effortless"

    # 2. THAILAND NATIONAL TEAM
    elif cat == 'Thailand National Team':
        attr = "เส้นใยทอพิเศษเกรดแข่งขัน + ตราช้างศึก 3D แท้ลิขสิทธิ์"
        func = "น้ำหนักเบา แห้งไว ไม่อมเหงื่อ ซักเครื่องได้ไม่ลอก"
        emot = "ภาคภูมิใจ ปลุกพลังเลือดนักสู้ มั่นใจทุกครั้งที่สวมใส่"
        ident = "แฟนบอลตัวจริงผู้มี Passion และสปอร์ตจิตวิญญาณแห่งชัยชนะ"

    # 3. RUNNING & SNEAKERS
    elif 'Shoes' in cat or 'Running' in cat or 'Sneakers' in cat:
        attr = "พื้นโฟม Cushioning ซับแรง + ผ้าถักหน้ากว้างระบายอากาศ"
        func = "นุ่มเด้ง ซัพพอร์ตอุ้งเท้าและส้นเท้า เดินทั้งวันไม่เมื่อย"
        emot = "หมดกังวลเรื่องปวดส้นเท้าหรือข้อเข่า เคลื่อนไหวได้อย่างอิสระ"
        ident = "สายแอคทีฟไลฟ์สไตล์ที่รักสุขภาพและใส่ใจคุณภาพชีวิต"

    # 4. PANTS & JEANS
    elif 'Pants' in cat or 'Jeans' in cat or 'Shorts' in cat:
        attr = "เนื้อผ้ายืดหยุ่น 4 ทิศ + ทรงกระบอกเล็กเข้ารูปกำลังดี"
        func = "ลุกนั่งสบายไม่รั้งเป้า คืนทรงไว ซักแล้วไม่ย้วย"
        emot = "มั่นใจในสรีระ ขาดูเรียวยาวขึ้นทันที พรางสะโพกได้เป๊ะ"
        ident = "ลุค Modern Casual มินิมอลมีสไตล์ แมตช์ได้กับทุกงาน"

    # 5. JACKETS & SUITS
    elif 'Jacket' in cat or 'Suit' in cat:
        attr = "ผ้าเบาพิเศษกันลมละอองน้ำ + คัตติ้งเนี้ยบระดับสูทสากล"
        func = "กันหนาวห้องแอร์ พับเก็บง่ายไม่ยับ พกพาสะดวก"
        emot = "พร้อมเสมอสำหรับทุกการประชุมหรือการเดินทางสำคัญ"
        ident = "ผู้นำรุ่นใหม่ บุคลิกสง่างาม คล่องตัวระดับมืออาชีพ"

    # 6. COMPRESSION & PERFORMANCE
    elif 'Compression' in cat or 'Tight' in name or 'Performance' in cat:
        attr = "ผ้ารัดกล้ามเนื้อ Spandex เกรดพรีเมียม ระบายอากาศรอบทิศ"
        func = "กระชับกล้ามเนื้อ ลดการสั่นไหว ป้องกันการบาดเจ็บ"
        emot = "มั่นใจในทุกการเคลื่อนไหว ดึงศักยภาพสูงสุดของร่างกาย"
        ident = "นักกีฬาและสายฟิตเนสตัวจริงที่มุ่งมั่นพัฒนาตัวเอง"

    # 7. DEFAULT / OVERSIZE
    else:
        attr = "ผ้าทอเส้นใยพรีเมียม + แพทเทิร์นสปอร์ตแคชชวลร่วมสมัย"
        func = "ใส่สบาย ระบายความร้อน แห้งไว ไม่ระคายเคืองผิว"
        emot = "ผ่อนคลาย สบายตัว มั่นใจในทุกกิจกรรมวันหยุด"
        ident = "คนรุ่นใหม่รักอิสระ สไตล์สปอร์ตมินิมอล คล่องตัวทุกวัน"

    p['value_ladder'] = {
        'level_1_attribute': attr,
        'level_2_functional': func,
        'level_3_emotional': emot,
        'level_4_identity': ident
    }
    return p

updated = [build_value_ladder(p) for p in products]

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(updated, f, ensure_ascii=False, indent=2)

print("Successfully generated 4-Level Fashion Value Ladder for all 100 SKUs!")
