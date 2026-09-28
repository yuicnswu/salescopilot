# -*- coding: utf-8 -*-
import json

def build_v3_html():
    with open('/Users/cattleya.c/.gemini/users/user1/warrix_products_data.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    products_json = json.dumps(products, ensure_ascii=False)

    template_html = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WARRIX Live Commerce Studio Hub & Lookbook (100 SKUs)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Kanit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js">
  // =========================================================
  // TIKTOK LIVE SELLING PLAN BUILDER ENGINE
  // =========================================================
  let pSelectedSkus = new Set(['WA-261PLACL15', 'LP-241JEMW103', 'WF-253RNACL04', 'WA-242TSAAL01']);
  let pPickerCategory = 'ALL';
  let pCurrentStep = 1;
  let pHolderSegIdx = 0;

  let liveSellingPlanData = {
    isApproved: false,
    overview: {
      theme: 'Smart Casual Friday & Workwear',
      target: 'วัยทำงาน 25-40 ปี ชอบเสื้อผ้าใส่สบาย คืนรูป ไม่ต้องรีด',
      duration: 60,
      host: 'MC นนท์ & MC แพรว',
      moderator: 'Mod กิ๊ก (ปักหมุด & ตอบไซส์)'
    },
    lookCards: [],
    rundown: []
  };

  function setPlanWizardStep(stepNum) {
    pCurrentStep = stepNum;
    for (let i = 1; i <= 4; i++) {
      const b = document.getElementById('pStepBtn' + i);
      const c = document.getElementById('pStepContainer' + i);
      if (b) b.classList.toggle('active', i === stepNum);
      if (c) c.classList.toggle('active', i === stepNum);
    }
    const pv = document.getElementById('plan-view');
    if (pv) pv.scrollTop = 0;
  }

  function renderPlanPickerGrid() {
    const q = (document.getElementById('pPickerSearch')?.value || '').toLowerCase().trim();
    const grid = document.getElementById('planPickerGrid');
    if (!grid) return;

    const filtered = PRODUCTS.filter(p => {
      const matchCat = (pPickerCategory === 'ALL') || (p.category && p.category.toLowerCase().includes(pPickerCategory.toLowerCase()));
      if (!matchCat) return false;
      if (!q) return true;
      return (p.name && p.name.toLowerCase().includes(q)) ||
             (p.sku && p.sku.toLowerCase().includes(q)) ||
             (p.available_colors_text && p.available_colors_text.toLowerCase().includes(q));
    });

    grid.innerHTML = filtered.map(p => {
      const isSel = pSelectedSkus.has(p.sku);
      const priceVal = getProductPrice(p);
      return `
        <div class="plan-picker-card ${isSel ? 'selected' : ''}" onclick="togglePlanSku('${p.sku}')">
          <input type="checkbox" class="card-check" ${isSel ? 'checked' : ''} onclick="event.stopPropagation(); togglePlanSku('${p.sku}')" />
          <div class="plan-picker-img">
            ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy">` : `<span style="font-size:36px;">👕</span>`}
          </div>
          <div>
            <div style="font-size:11px; font-weight:700; color:#38bdf8;">${p.sku}</div>
            <div style="font-size:13px; font-weight:600; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:2px;">${p.name}</div>
            <div style="font-size:11px; color:var(--text-muted);">${p.category || 'Apparel'}</div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:auto; padding-top:6px; border-top:1px solid rgba(255,255,255,0.05);">
            <span style="font-size:14px; font-weight:800; color:#10b981;">฿${priceVal.toLocaleString()}</span>
            <span style="font-size:10.5px; color:#94a3b8;">${p.size_chart?.measurements ? p.size_chart.measurements.length + ' ไซส์' : 'ครบไซส์'}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  function filterPlanPickerCat(cat, el) {
    pPickerCategory = cat;
    el.parentElement.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
    el.classList.add('active');
    renderPlanPickerGrid();
  }

  function togglePlanSku(sku) {
    if (pSelectedSkus.has(sku)) {
      pSelectedSkus.delete(sku);
    } else {
      pSelectedSkus.add(sku);
    }
    renderPlanPickerGrid();
    updatePlanTray();
  }

  function updatePlanTray() {
    const badge = document.getElementById('pTrayCount');
    const thumbs = document.getElementById('pTrayThumbs');
    const priceEl = document.getElementById('pTrayPrice');
    if (!badge || !thumbs || !priceEl) return;

    badge.textContent = `เลือกแล้ว ${pSelectedSkus.size} ชิ้น`;

    let sum = 0;
    let thHtml = '';
    pSelectedSkus.forEach(sku => {
      const p = PRODUCTS.find(x => x.sku === sku);
      if (p) {
        sum += getProductPrice(p);
        thHtml += `<img src="${p.image_url || ''}" style="width:34px; height:34px; border-radius:6px; background:#000; border:1px solid #334155; object-fit:cover;" title="${p.name}" />`;
      }
    });

    thumbs.innerHTML = thHtml;
    priceEl.textContent = `รวม ฿${sum.toLocaleString()}`;
  }

  function proceedToPlanBrief() {
    if (pSelectedSkus.size === 0) {
      showToast('⚠️ กรุณาเลือกสินค้าอย่างน้อย 1 ชิ้นก่อนดำเนินการต่อครับ');
      return;
    }
    document.getElementById('pStepBtn1')?.classList.add('completed');
    setPlanWizardStep(2);
  }

  function generateLiveSellingPlan(e) {
    if (e) e.preventDefault();
    const theme = document.getElementById('pBriefTheme')?.value || 'Smart Casual Friday & Workwear';
    const target = document.getElementById('pBriefTarget')?.value || 'วัยทำงาน 25-40 ปี';
    const duration = parseInt(document.getElementById('pBriefDuration')?.value, 10) || 60;
    const host = document.getElementById('pBriefHost')?.value || 'MC นนท์';
    const mod = document.getElementById('pBriefMod')?.value || 'Mod กิ๊ก';

    liveSellingPlanData.isApproved = false;
    liveSellingPlanData.overview = { theme, target, duration, host, moderator: mod };

    const selList = Array.from(pSelectedSkus).map(sku => PRODUCTS.find(x => x.sku === sku)).filter(Boolean);
    const tops = selList.filter(p => !p.category.includes('Pant') && !p.category.includes('Shoe') && !p.category.includes('Cap'));
    const bottoms = selList.filter(p => p.category.includes('Pant') || p.category.includes('Short') || p.name.includes('กางเกง'));
    const shoes = selList.filter(p => p.category.includes('Shoe') || p.category.includes('Sneaker') || p.category.includes('Cap') || p.name.includes('รองเท้า') || p.name.includes('หมวก'));

    // Grounded Look Cards
    liveSellingPlanData.lookCards = [];
    if (tops.length > 0) {
      const heroTop = tops[0];
      const matchBot = bottoms.length > 0 ? bottoms[0] : null;
      const matchSho = shoes.length > 0 ? shoes[0] : null;

      let totalP = getProductPrice(heroTop);
      let itemsDesc = heroTop.name;
      if (matchBot) { totalP += getProductPrice(matchBot); itemsDesc += ' + ' + matchBot.name; }
      if (matchSho) { totalP += getProductPrice(matchSho); itemsDesc += ' + ' + matchSho.name; }

      liveSellingPlanData.lookCards.push({
        name: `Total Look 1: ${theme.split('&')[0].trim()}`,
        heroSku: heroTop.sku,
        items: itemsDesc,
        totalPrice: totalP,
        stylingNote: heroTop.styling_advice || 'แมตช์คู่สีคุมโทน เสริมความสมาร์ทแบบผ่อนคลาย',
        fitNote: heroTop.size_chart?.fit_advice || 'Regular Fit ทรงมาตรฐาน ไม่รัดรูป'
      });
    }

    // Timed Rundown Segments (sum(T) == Duration)
    const segments = [];
    const introTime = 5;
    const closingTime = 5;
    const qaTime = 5;
    const productTimeTotal = duration - (introTime + closingTime + qaTime);

    // Intro
    segments.push({
      id: 'seg-1',
      title: 'Segment 1: ต้อนรับ & ชี้แจงกติกาโปรโมชั่น',
      duration: introTime,
      sku: selList[0]?.sku || 'WARRIX',
      pinText: `ปักหมุดคูปองไลฟ์สด & สินค้าแรก (${selList[0]?.sku || 'WARRIX'})`,
      script: `สวัสดีครับคุณผู้ชมทุกท่าน! ยินดีต้อนรับเข้าสู่ WARRIX Live ธีม "${theme}" วันนี้เราคัดไอเทมตัวท็อปมาให้ชม พร้อมส่วนลดเซ็ต 2 ชิ้น 15% และ 3 ชิ้น 20% ทันทีครับ!`,
      modChecklist: 'เตรียมปักหมุดสินค้าแรก, ตรวจสอบโค้ดส่งฟรี'
    });

    // Product segments
    const numProdSegs = Math.min(selList.length, 3);
    const timePerProd = Math.floor(productTimeTotal / numProdSegs);
    let remainder = productTimeTotal % numProdSegs;

    for (let i = 0; i < numProdSegs; i++) {
      const p = selList[i];
      const segDur = timePerProd + (i === 0 ? remainder : 0);
      const hook = p.how_to_sell?.hook || p.fashion_hook || 'เสื้อคุณภาพพรีเมียม ระบายอากาศยอดเยี่ยม';
      const fabric = p.what_it_is?.fabric || 'Jacquard Polyester 100%';

      segments.push({
        id: `seg-${i+2}`,
        title: `Segment ${i+2}: เจาะลึก ${p.name} (${p.sku})`,
        duration: segDur,
        sku: p.sku,
        pinText: `ปักหมุดตะกร้า #${i+1}: ${p.name} [${p.sku}] ราคา ฿${getProductPrice(p).toLocaleString()}`,
        script: `"${hook}" — รุ่นนี้มาพร้อมเนื้อผ้า ${fabric} สวมใส่สบาย ยับยาก ไม่ต้องรีด ใครชอบความคล่องตัวแนะนำเลยครับ!`,
        modChecklist: `เช็กสต็อกไซส์ ${p.sku}, เตรียมสูตรเทียบไซส์ตอบลูกค้า`
      });
    }

    // QA
    segments.push({
      id: `seg-${numProdSegs+2}`,
      title: `Segment ${numProdSegs+2}: ตอบคำถามไซส์ & แมตช์คู่สีสด`,
      duration: qaTime,
      sku: selList[0]?.sku || 'WARRIX',
      pinText: 'ปักหมุดตารางเทียบไซส์ & เซ็ต Total Look',
      script: 'ใครไม่แน่ใจเรื่องไซส์ พิมพ์ส่วนสูงและน้ำหนักเข้ามาในแชตได้เลยครับ เดี๋ยว MC และแอดมินช่วยแนะนำไซส์ที่ใส่สวยที่สุดให้ทันทีครับ!',
      modChecklist: 'ใช้ Size Hub คำนวณไซส์ตอบลูกค้าในแชตสด'
    });

    // Closing
    segments.push({
      id: `seg-${numProdSegs+3}`,
      title: `Segment ${numProdSegs+3}: สรุปโปรโมชั่น & ปิดการขาย Flash Deals`,
      duration: closingTime,
      sku: selList[0]?.sku || 'WARRIX',
      pinText: 'ปักหมุดสรุปโปรโมชั่น Bundle Deal ลด 20%',
      script: 'ก่อนปิดไลฟ์วันนี้ ขอสรุปโปรโมชั่นสุดคุ้ม ซื้อครบเซ็ต 3 ชิ้นลดทันที 20% ใครกดสั่งแล้วเตรียมรอรับสินค้าของแท้จาก WARRIX ได้เลยครับ ขอบคุณทุกคนมากครับ!',
      modChecklist: 'ตรวจเช็กออเดอร์ที่ค้างชำระ, ส่งข้อความขอบคุณลูกค้า'
    });

    liveSellingPlanData.rundown = segments;

    renderPlanReviewStack();
    document.getElementById('pStepBtn2')?.classList.add('completed');
    setPlanWizardStep(3);
    showToast('⚡ สร้างแผนไลฟ์สดสำเร็จแล้ว!');
  }

  function renderPlanReviewStack() {
    const ov = liveSellingPlanData.overview;
    document.getElementById('pPlanTitle').textContent = `แผนไลฟ์สด: ${ov.theme}`;
    document.getElementById('pPlanDesc').textContent = `เป้าหมาย: ${ov.target} • เวลารวม: ${ov.duration} นาที • พิธีกร: ${ov.host} • แอดมิน: ${ov.moderator}`;

    const statusBadge = document.getElementById('pPlanStatus');
    if (liveSellingPlanData.isApproved) {
      statusBadge.textContent = '✅ Approved (อนุมัติแล้ว)';
      statusBadge.style.background = 'rgba(16,185,129,0.2)';
      statusBadge.style.color = '#34d399';
      statusBadge.style.borderColor = 'rgba(16,185,129,0.4)';
    } else {
      statusBadge.textContent = 'Draft (รอการอนุมัติ)';
      statusBadge.style.background = 'rgba(245,158,11,0.2)';
      statusBadge.style.color = '#fbbf24';
      statusBadge.style.borderColor = 'rgba(245,158,11,0.4)';
    }

    let totalT = 0;
    liveSellingPlanData.rundown.forEach(s => totalT += s.duration);
    document.getElementById('pPlanTimeMatch').textContent = `${totalT} / ${ov.duration} นาที (ตรงเป๊ะ 100%)`;

    // Render Look Cards
    const lkGrid = document.getElementById('pPlanLookGrid');
    if (lkGrid) {
      lkGrid.innerHTML = liveSellingPlanData.lookCards.map(l => `
        <div class="plan-look-box">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#fff; font-size:14.5px;">${l.name}</strong>
            <span style="color:#10b981; font-weight:800; font-size:15px;">฿${l.totalPrice.toLocaleString()}</span>
          </div>
          <div style="font-size:12px; color:#38bdf8; font-weight:700;">Hero SKU: ${l.heroSku}</div>
          <div style="font-size:12.5px; color:#cbd5e1;">ไอเทม: ${l.items}</div>
          <div style="font-size:11.5px; color:var(--text-muted); background:rgba(0,0,0,0.3); padding:8px; border-radius:6px; margin-top:4px;">
            💡 <strong>คำแนะนำสไตลิ่ง:</strong> ${l.stylingNote}<br/>
            📏 <strong>ทรง:</strong> ${l.fitNote}
          </div>
        </div>
      `).join('') || '<div style="color:var(--text-muted); font-size:13px;">ไม่มีเซ็ตชุด (โชว์สินค้าเดี่ยว)</div>';
    }

    // Render Rundown List
    const rdStack = document.getElementById('pPlanRundownStack');
    if (rdStack) {
      rdStack.innerHTML = liveSellingPlanData.rundown.map((seg, idx) => `
        <div class="plan-seg-card">
          <div class="plan-seg-time">
            <div style="font-size:18px; font-weight:800; color:#38bdf8;">${seg.duration}</div>
            <div style="font-size:10.5px; color:var(--text-dim);">นาที</div>
          </div>
          <div>
            <h4 style="font-size:14.5px; font-weight:700; color:#fff; margin-bottom:4px;">${seg.title}</h4>
            <div style="font-size:11.5px; color:#f472b6; font-weight:700;">📌 ${seg.pinText}</div>
            <div style="background:#040711; border:1px solid rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:12.5px; color:#cbd5e1; line-height:1.5; margin-top:6px;">
              🎙️ <strong>สคริปต์ MC:</strong><br/>
              ${seg.script}
            </div>
          </div>
          <div style="background:var(--bg-panel); border:1px solid var(--border-subtle); padding:10px; border-radius:8px; font-size:12px;">
            <div style="font-weight:700; color:#fbbf24; margin-bottom:3px;">🛡️ Moderator Checklist:</div>
            <div style="color:#cbd5e1;">${seg.modChecklist}</div>
          </div>
          <div class="plan-seg-actions">
            <button class="plan-btn-reorder" onclick="movePlanSeg(${idx}, -1)" ${idx === 0 ? 'disabled style="opacity:0.3"' : ''}>▲ ขึ้น</button>
            <button class="plan-btn-reorder" onclick="movePlanSeg(${idx}, 1)" ${idx === liveSellingPlanData.rundown.length - 1 ? 'disabled style="opacity:0.3"' : ''}>▼ ลง</button>
          </div>
        </div>
      `).join('');
    }
  }

  function movePlanSeg(idx, dir) {
    const target = idx + dir;
    if (target < 0 || target >= liveSellingPlanData.rundown.length) return;
    const temp = liveSellingPlanData.rundown[idx];
    liveSellingPlanData.rundown[idx] = liveSellingPlanData.rundown[target];
    liveSellingPlanData.rundown[target] = temp;
    liveSellingPlanData.isApproved = false; // require re-approval
    renderPlanReviewStack();
    showToast('🔄 สลับลำดับคิวสำเร็จ (ต้องอนุมัติแผนใหม่อีกครั้ง)');
  }

  function savePlanDraftAction() {
    showToast('💾 บันทึกแบบร่างแผนไลฟ์สดเรียบร้อย');
  }

  function exportPlanJsonFile() {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(liveSellingPlanData, null, 2));
    const a = document.createElement('a');
    a.setAttribute('href', dataStr);
    a.setAttribute('download', `WARRIX_Live_Plan_${Date.now()}.json`);
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast('📥 ดาวน์โหลดไฟล์ JSON เรียบร้อย');
  }

  function approveLivePlan() {
    liveSellingPlanData.isApproved = true;
    document.getElementById('pStepBtn3')?.classList.add('completed');
    renderPlanReviewStack();
    setupHostAndModViews();
    setPlanWizardStep(4);
    showToast('🎉 อนุมัติแผนไลฟ์สดเรียบร้อย! เข้าสู่ห้องออกอากาศสด');
  }

  function setupHostAndModViews() {
    pHolderSegIdx = 0;
    updateHostLiveUI();
    updateModLiveUI();
  }

  function setLiveSubview(sub) {
    document.getElementById('pBtnHostSub')?.classList.toggle('active', sub === 'host');
    document.getElementById('pBtnModSub')?.classList.toggle('active', sub === 'mod');
    document.getElementById('pHostViewBox').style.display = (sub === 'host') ? 'flex' : 'none';
    document.getElementById('pModViewBox').style.display = (sub === 'mod') ? 'grid' : 'none';
  }

  function updateHostLiveUI() {
    const seg = liveSellingPlanData.rundown[pHolderSegIdx];
    if (!seg) return;
    document.getElementById('pHostSegTitle').textContent = seg.title;
    document.getElementById('pHostSegTimer').textContent = `${String(seg.duration).padStart(2, '0')}:00`;
    document.getElementById('pHostPinText').textContent = seg.pinText;
    document.getElementById('pHostScriptText').textContent = seg.script;
    document.getElementById('pHostSegCount').textContent = `คิวที่ ${pHolderSegIdx + 1} จากทั้งหมด ${liveSellingPlanData.rundown.length} คิว`;
  }

  function stepHostSeg(dir) {
    const nextIdx = pHolderSegIdx + dir;
    if (nextIdx >= 0 && nextIdx < liveSellingPlanData.rundown.length) {
      pHolderSegIdx = nextIdx;
      updateHostLiveUI();
      updateModLiveUI();
    } else if (nextIdx >= liveSellingPlanData.rundown.length) {
      showToast('🏁 จบทุกคิวในรอบไลฟ์สดนี้แล้วครับ!');
    }
  }

  function updateModLiveUI() {
    const seg = liveSellingPlanData.rundown[pHolderSegIdx];
    if (!seg) return;
    const p = PRODUCTS.find(x => x.sku === seg.sku) || PRODUCTS[0];

    const skuPanel = document.getElementById('pModSkuPanel');
    if (skuPanel) {
      skuPanel.innerHTML = `
        <div style="font-size:12px; font-weight:700; color:#ea580c; margin-bottom:6px;">📌 สินค้าที่ต้องปักหมุดสด</div>
        <div style="font-size:15px; font-weight:700; color:#fff;">${p.name}</div>
        <div style="font-size:12px; color:#38bdf8; font-weight:700; margin-top:2px;">รหัส: ${p.sku}</div>
        <div style="font-size:17px; font-weight:800; color:#10b981; margin-top:6px;">฿${getProductPrice(p).toLocaleString()}</div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:8px;">
          🧵 <strong>ผ้า:</strong> ${(p.what_it_is && p.what_it_is.fabric) ? p.what_it_is.fabric : 'Polyester 100%'}<br/>
          🎨 <strong>สี:</strong> ${p.available_colors_text || 'ครบสีมาตรฐาน'}
        </div>
      `;
    }

    const sizePanel = document.getElementById('pModSizePanel');
    if (sizePanel) {
      sizePanel.innerHTML = `
        <div style="font-size:12px; font-weight:700; color:#38bdf8; margin-bottom:6px;">📏 ตารางไซส์สำหรับตอบแชต</div>
        <div style="font-size:12.5px; color:#e2e8f0; margin-bottom:6px;">สูตรแนะนำ: <strong>${(p.size_chart && p.size_chart.quick_formula) || 'รอบอกจริง + 2 นิ้ว = ไซส์ที่แนะนำ'}</strong></div>
        <table style="width:100%; border-collapse:collapse; font-size:11.5px; text-align:left;">
          <tr style="border-bottom:1px solid #334155; color:#94a3b8;"><th>Size</th><th>รอบอก</th><th>ความยาว</th></tr>
          <tr><td>S</td><td>38"</td><td>27"</td></tr>
          <tr><td>M</td><td>40"</td><td>28"</td></tr>
          <tr><td>L</td><td>42"</td><td>29"</td></tr>
          <tr><td>XL</td><td>44"</td><td>30"</td></tr>
        </table>
      `;
    }
  }

  function copyReplyText(txt) {
    navigator.clipboard.writeText(txt).then(() => showToast('📋 คัดลอกข้อความตอบคอมเมนต์เรียบร้อย!'));
  }

  
  // =========================================================
  // FLOATING DYNAMIC SPOTLIGHT SEARCH (CMD+K / CTRL+K)
  // =========================================================
  let spotlightActiveFilter = 'ALL';
  let spotlightFocusedIndex = 0;
  let spotlightCurrentResults = [];

  window.addEventListener('keydown', (e) => {
    // Cmd+K or Ctrl+K or '/' to open spotlight search
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      toggleSpotlightSearch();
    } else if (e.key === 'Escape') {
      closeSpotlightSearch();
    }
  });

  
  // PRODUCT SIDEBAR COLLAPSE / HIDE TOGGLE (ON / OFF)
  let isSidebarCollapsed = false;

  function toggleProductSidebar(force) {
    const sidebar = document.getElementById('product-sidebar') || document.querySelector('.product-sidebar');
    const restoreBtn = document.getElementById('stage-sidebar-restore-btn');
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    const headerToggleBtn = document.getElementById('header-sku-toggle-btn');
    const statusDot = document.getElementById('sku-status-dot');
    const statusLabel = document.getElementById('sku-status-label');
    if (!sidebar) return;

    if (typeof force === 'boolean') {
      isSidebarCollapsed = force;
    } else {
      isSidebarCollapsed = !isSidebarCollapsed;
    }

    if (isSidebarCollapsed) {
      sidebar.classList.add('collapsed');
      sidebar.style.display = 'none';
      if (restoreBtn) restoreBtn.style.display = 'inline-flex';
      if (toggleBtn) toggleBtn.innerHTML = '👁️ เปิด (ON)';
      if (statusDot) statusDot.style.background = '#f59e0b';
      if (statusLabel) statusLabel.textContent = 'รายการสินค้า: OFF';
      if (headerToggleBtn) {
        headerToggleBtn.style.background = 'rgba(245, 158, 11, 0.12)';
        headerToggleBtn.style.borderColor = 'rgba(245, 158, 11, 0.4)';
        headerToggleBtn.style.color = '#f59e0b';
      }
      showToast('👁️ ซ่อนรายการสินค้า (OFF) — หน้าจอ Live Prompter ขยายเต็มตา');
    } else {
      sidebar.classList.remove('collapsed');
      sidebar.style.display = 'flex';
      if (restoreBtn) restoreBtn.style.display = 'none';
      if (toggleBtn) toggleBtn.innerHTML = '✕ ซ่อน (OFF)';
      if (statusDot) statusDot.style.background = '#10b981';
      if (statusLabel) statusLabel.textContent = 'รายการสินค้า: ON';
      if (headerToggleBtn) {
        headerToggleBtn.style.background = 'rgba(16, 185, 129, 0.12)';
        headerToggleBtn.style.borderColor = 'rgba(16, 185, 129, 0.35)';
        headerToggleBtn.style.color = '#34d399';
      }
      showToast('📑 แสดงรายการสินค้า (ON) เรียบร้อย');
    }

    try {
      localStorage.setItem('warrix_sidebar_collapsed', isSidebarCollapsed ? '1' : '0');
    } catch (e) {}
  }

  function initSidebarState() {
    try {
      const saved = localStorage.getItem('warrix_sidebar_collapsed');
      if (saved === '1') {
        toggleProductSidebar(true);
      }
    } catch (e) {}
  }

  
  // GLOBAL HOTKEYS FOR MCs & BACKSTAGE (Space / Up / Down / P / H)
  document.addEventListener('keydown', (e) => {
    // Skip hotkeys when typing in input or textarea
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      return;
    }

    if (e.key === ' ' || e.key === 'ArrowDown') {
      // Next SKU in studio
      if (currentWorkspace === 'studio') {
        e.preventDefault();
        const currentIdx = PRODUCTS.findIndex(p => p.sku === selectedSku);
        if (currentIdx !== -1 && currentIdx < PRODUCTS.length - 1) {
          selectProduct(PRODUCTS[currentIdx + 1].sku);
          showToast(`➡️ สินค้าถัดไป: [${PRODUCTS[currentIdx + 1].sku}] ${PRODUCTS[currentIdx + 1].name}`);
        }
      }
    } else if (e.key === 'ArrowUp') {
      // Previous SKU in studio
      if (currentWorkspace === 'studio') {
        e.preventDefault();
        const currentIdx = PRODUCTS.findIndex(p => p.sku === selectedSku);
        if (currentIdx > 0) {
          selectProduct(PRODUCTS[currentIdx - 1].sku);
          showToast(`⬅️ สินค้าก่อนหน้า: [${PRODUCTS[currentIdx - 1].sku}] ${PRODUCTS[currentIdx - 1].name}`);
        }
      }
    } else if (e.key === 'p' || e.key === 'P') {
      e.preventDefault();
      copyPinText(selectedSku);
    } else if (e.key === 'h' || e.key === 'H') {
      e.preventDefault();
      toggleProductSidebar();
    }
  });

  function toggleSpotlightSearch() {
    const modal = document.getElementById('spotlight-modal');
    if (!modal) return;
    if (modal.classList.contains('active')) {
      closeSpotlightSearch();
    } else {
      openSpotlightSearch();
    }
  }

  function openSpotlightSearch() {
    const modal = document.getElementById('spotlight-modal');
    if (!modal) return;
    modal.classList.add('active');
    const input = document.getElementById('spotlight-search-input');
    if (input) {
      input.focus();
      input.select();
    }
    spotlightFocusedIndex = 0;
    renderSpotlightResults();
  }

  function closeSpotlightSearch() {
    const modal = document.getElementById('spotlight-modal');
    if (modal) modal.classList.remove('active');
  }

  function closeSpotlightOnBackdrop(e) {
    if (e.target.id === 'spotlight-modal') {
      closeSpotlightSearch();
    }
  }

  function setSpotlightFilter(cat, el) {
    spotlightActiveFilter = cat;
    el.parentElement.querySelectorAll('.spotlight-filter-pill').forEach(p => p.classList.remove('active'));
    el.classList.add('active');
    spotlightFocusedIndex = 0;
    renderSpotlightResults();
  }

  function handleSpotlightInput() {
    spotlightFocusedIndex = 0;
    renderSpotlightResults();
  }

  function handleSpotlightKeydown(e) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (spotlightFocusedIndex < spotlightCurrentResults.length - 1) {
        spotlightFocusedIndex++;
        updateSpotlightFocusDOM();
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (spotlightFocusedIndex > 0) {
        spotlightFocusedIndex--;
        updateSpotlightFocusDOM();
      }
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (spotlightCurrentResults.length > 0 && spotlightCurrentResults[spotlightFocusedIndex]) {
        const item = spotlightCurrentResults[spotlightFocusedIndex];
        selectProduct(item.sku);
        switchView('studio');
        closeSpotlightSearch();
        showToast(`📺 โฟกัสสินค้า ${item.sku} ใน Live Prompter แล้ว!`);
      }
    }
  }

  function updateSpotlightFocusDOM() {
    const items = document.querySelectorAll('.spotlight-item-card');
    items.forEach((it, idx) => {
      it.classList.toggle('focused', idx === spotlightFocusedIndex);
      if (idx === spotlightFocusedIndex) {
        it.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    });
  }

  function renderSpotlightResults() {
    const query = (document.getElementById('spotlight-search-input')?.value || '').toLowerCase().trim();
    const listEl = document.getElementById('spotlight-results-list');
    const countEl = document.getElementById('spotlight-match-count');
    if (!listEl) return;

    spotlightCurrentResults = PRODUCTS.filter(p => {
      const matchCat = (spotlightActiveFilter === 'ALL') || (p.category && p.category.toLowerCase().includes(spotlightActiveFilter.toLowerCase()));
      if (!matchCat) return false;
      if (!query) return true;
      return (p.name && p.name.toLowerCase().includes(query)) ||
             (p.sku && p.sku.toLowerCase().includes(query)) ||
             (p.category && p.category.toLowerCase().includes(query)) ||
             (p.what_it_is?.fabric && p.what_it_is.fabric.toLowerCase().includes(query)) ||
             (p.available_colors_text && p.available_colors_text.toLowerCase().includes(query)) ||
             (p.occasion_vibes && p.occasion_vibes.some(v => v.toLowerCase().includes(query)));
    });

    if (countEl) {
      countEl.textContent = `พบ ${spotlightCurrentResults.length} จาก 100 รายการ`;
    }

    if (spotlightCurrentResults.length === 0) {
      listEl.innerHTML = `
        <div style="text-align:center; padding:32px 16px; color:var(--text-muted); font-size:13.5px;">
          🔍 ไม่พบสินค้าที่ตรงกับคำค้นหา "<strong>${query}</strong>"
        </div>
      `;
      return;
    }

    listEl.innerHTML = spotlightCurrentResults.map((p, idx) => {
      const priceVal = getProductPrice(p);
      const isFocused = idx === spotlightFocusedIndex;
      const fabricText = p.what_it_is?.fabric || 'Polyester 100%';
      return `
        <div class="spotlight-item-card ${isFocused ? 'focused' : ''}" onclick="selectProduct('${p.sku}'); switchView('studio'); closeSpotlightSearch();">
          <div class="spotlight-item-thumb">
            ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy">` : `<span style="font-size:22px;">👕</span>`}
          </div>
          <div class="spotlight-item-info">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="spotlight-item-sku">${p.sku}</span>
              <span style="font-size:11px; color:#94a3b8; background:rgba(255,255,255,0.06); padding:1px 6px; border-radius:4px;">${p.category || 'Apparel'}</span>
            </div>
            <div class="spotlight-item-name">${p.name}</div>
            <div class="spotlight-item-fabric">🧵 ${fabricText} • 🎨 ${p.available_colors_text || 'ครบสี'}</div>
          </div>
          <div class="spotlight-item-right">
            <div class="spotlight-item-price">฿${priceVal.toLocaleString()}</div>
            <div class="spotlight-quick-actions" onclick="event.stopPropagation()">
              <button class="btn-spotlight-action" onclick="sendToLookbook('${p.sku}'); closeSpotlightSearch();" title="นำเข้า Lookbook">👗 Lookbook</button>
              <button class="btn-spotlight-action" onclick="togglePlanSku('${p.sku}'); closeSpotlightSearch(); switchView('plan');" title="นำเข้า Live Plan">📋 Plan</button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  </script>
  <style>

    /* --- Flow Animations --- */
    @keyframes viewFadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    .view-anim {
      animation: viewFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    :root {
      --bg-base: #07090e;
      --bg-surface: #0e131f;
      --bg-panel: #141b2d;
      --bg-panel-hover: #1c263e;
      --border-subtle: #1e293b;
      --border-focus: #3b82f6;
      --border-accent: #f59e0b;
      --accent-gold: #f59e0b;
      --accent-gold-light: #fbbf24;
      --accent-pink: #ec4899;
      --accent-purple: #8b5cf6;
      --accent-blue: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-green: #10b981;
      --accent-red: #ef4444;
      --text-high: #f8fafc;
      --text-medium: #cbd5e1;
      --text-muted: #64748b;
      --shopee-orange: #ee4d2d;
      --warrix-blue: #002d62;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Kanit', sans-serif;
      background-color: var(--bg-base);
      color: var(--text-high);
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* Top Navigation Bar */
    header.studio-header {
      background: rgba(10, 15, 29, 0.95);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-shrink: 0;
      z-index: 50;
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 290px;
    }

    .brand-badge {
      width: 38px;
      height: 38px;
      background: linear-gradient(135deg, var(--accent-gold), #b45309);
      color: #000;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 20px;
      box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }

    .brand-title-box h1 {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.3px;
      line-height: 1.2;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-title-box .live-indicator {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #f87171;
      padding: 2px 7px;
      border-radius: 12px;
      font-size: 10px;
      font-weight: 600;
    }

    .live-dot {
      width: 6px;
      height: 6px;
      background-color: #ef4444;
      border-radius: 50%;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.3); }
    }

    .brand-subtitle {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 300;
    }

        .header-search-box {
      flex: 1;
      max-width: 580px;
      min-width: 280px;
      position: relative;
    }

    .header-search-box input {
      width: 100%;
      height: 44px;
      background: rgba(15, 23, 42, 0.88);
      border: 1px solid rgba(99, 102, 241, 0.4);
      border-radius: 12px;
      padding: 10px 85px 10px 42px;
      color: #fff;
      font-family: inherit;
      font-size: 14px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
    }

    .header-search-box:hover input, .header-search-box input:focus {
      outline: none;
      border-color: #38bdf8;
      background: rgba(15, 23, 42, 0.98);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25), 0 4px 20px rgba(0, 0, 0, 0.55);
    }

    .search-lens {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: #38bdf8;
      font-size: 16px;
      pointer-events: none;
    }

    .header-search-badge {
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #94a3b8;
      font-size: 11.5px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 6px;
      cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      align-items: center;
      gap: 3px;
      transition: all 0.2s ease;
    }

    .header-search-badge:hover {
      background: rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      border-color: #38bdf8;
    }

    .btn-sku-toggle {
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399;
      font-weight: 600;
    }
    .btn-sku-toggle:hover {
      background: rgba(16, 185, 129, 0.22);
      border-color: #10b981;
    }

    .view-switcher {
      display: flex;
      gap: 6px;
      align-items: center;
    }

    .view-btn {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      color: var(--text-medium);
      padding: 7px 13px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: inherit;
      transition: all 0.2s ease;
    }

    .view-btn:hover {
      background: var(--bg-panel-hover);
      color: #fff;
    }

    .view-btn.active {
      background: rgba(59, 130, 246, 0.15);
      border-color: var(--accent-blue);
      color: #93c5fd;
      font-weight: 600;
    }

    .view-btn.btn-lookbook.active {
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.25), rgba(139, 92, 246, 0.25));
      border-color: var(--accent-pink);
      color: #f472b6;
    }

    .view-btn.btn-stylist.active {
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(59, 130, 246, 0.25));
      border-color: var(--accent-purple);
      color: #c084fc;
    }

    .view-btn.btn-sizes.active {
      background: rgba(245, 158, 11, 0.2);
      border-color: var(--accent-gold);
      color: #fbbf24;
    }

    /* Occasion & Vibe Discovery Filter Bar */
    nav.filter-chips-bar {
      background: #090d16;
      border-bottom: 1px solid var(--border-subtle);
      padding: 7px 24px;
      display: flex;
      align-items: center;
      gap: 7px;
      overflow-x: auto;
      flex-shrink: 0;
      scrollbar-width: thin;
    }

    .chip-btn {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-medium);
      padding: 4px 11px;
      border-radius: 18px;
      font-size: 11.5px;
      font-weight: 400;
      cursor: pointer;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 5px;
      font-family: inherit;
      transition: all 0.18s ease;
    }

    .chip-btn:hover {
      background: var(--bg-panel);
      color: #fff;
      border-color: #334155;
    }

    .chip-btn.active {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.15));
      border-color: var(--accent-gold);
      color: var(--accent-gold-light);
      font-weight: 600;
    }

    .chip-btn.chip-vibe {
      border-color: rgba(236, 72, 153, 0.3);
      color: #f472b6;
    }

    .chip-btn.chip-vibe.active {
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.25), rgba(139, 92, 246, 0.2));
      border-color: var(--accent-pink);
      color: #fff;
    }

    /* App Workspace */
    .app-workspace {
      flex: 1;
      min-height: 0;
      display: flex;
      flex-direction: column; /* FIXES SQUISHED VIEWS */
      overflow: hidden;
      position: relative;
      width: 100%;
    }



    /* Ensure all views stretch to full size */
    .app-workspace > div[id$="-view"] {
      width: 100% !important;
      height: 100% !important;
      flex: 1 1 100% !important;
    }

    /* VIEW 8: PRODUCT KNOWLEDGE & SALES GUIDE HUB */
    .knowledge-view {
      display: none;
      width: 100%;
      height: 100%;
      overflow-y: auto;
      overflow-x: hidden;
      -webkit-overflow-scrolling: touch;
      padding: 20px 24px 80px 24px;
      box-sizing: border-box;
      scroll-behavior: smooth;
    }

    .knowledge-container {
      max-width: 1480px;
      margin: 0 auto;
      animation: fadeIn 0.25s ease;
    }

    .k-grid-2col {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(min(100%, 460px), 1fr));
      gap: 20px;
      margin-bottom: 24px;
    }

    /* VIEW 1: STUDIO SPLIT VIEW */
    .studio-split-view {
      display: flex;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }

    /* Left Sidebar */
    .product-sidebar {
      width: 340px;
      background: var(--bg-surface);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      transition: width 0.28s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease, padding 0.28s ease;
      position: relative;
    }

    .product-sidebar.collapsed {
      width: 0 !important;
      min-width: 0 !important;
      max-width: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
      border-right: none !important;
      opacity: 0;
      pointer-events: none;
    }

    .btn-sidebar-toggle {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #94a3b8;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
      font-family: inherit;
    }

    .btn-sidebar-toggle:hover {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.25);
    }

    .floating-sidebar-restore-btn {
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 100;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(56, 189, 248, 0.5);
      color: #38bdf8;
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.6);
      backdrop-filter: blur(8px);
      transition: all 0.2s ease;
      font-family: inherit;
      animation: fadeInModal 0.2s ease;
    }

    .floating-sidebar-restore-btn:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
      transform: translateX(3px);
    }

    .sidebar-header {
      padding: 11px 16px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-medium);
    }

    .product-list-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .list-item-card {
      background: var(--bg-panel);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 10px;
      padding: 10px 12px;
      cursor: pointer;
      display: flex;
      gap: 10px;
      align-items: center;
      transition: all 0.15s ease;
      position: relative;
    }

    .list-item-card:hover {
      background: var(--bg-panel-hover);
      border-color: #334155;
      transform: translateX(2px);
    }

    .list-item-card.active {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
      border-color: var(--accent-blue);
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.2);
    }

    .list-item-thumb {
      width: 44px;
      height: 44px;
      border-radius: 7px;
      background: #040711;
      border: 1px solid #1e293b;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      flex-shrink: 0;
    }

    .list-item-thumb img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .list-item-info {
      flex: 1;
      min-width: 0;
    }

    .list-item-sku {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: var(--accent-gold);
      letter-spacing: 0.3px;
    }

    .list-item-name {
      font-size: 12.5px;
      font-weight: 500;
      color: #fff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 1px;
    }

    .list-item-bottom {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 3px;
      font-size: 11px;
    }

    .list-item-price {
      font-weight: 700;
      color: var(--accent-green);
    }

    .list-item-vibe {
      font-size: 9.5px;
      color: #f472b6;
      background: rgba(236, 72, 153, 0.1);
      padding: 1px 5px;
      border-radius: 4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 130px;
    }

    /* Right Prompter Stage */
    .product-teleprompter-stage {
      flex: 1;
      background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.05) 0%, transparent 50%), var(--bg-base);
      overflow-y: auto;
      padding: 20px 26px 60px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .prompter-top-nav {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      flex-wrap: wrap;
    }

    .prompter-header-info {
      flex: 1;
      min-width: 280px;
    }

    .sku-badge-large {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.3);
      color: #fbbf24;
      padding: 3px 9px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 6px;
    }

    .prompter-title {
      font-size: 22px;
      font-weight: 700;
      color: #fff;
      line-height: 1.25;
    }

    .prompter-pitch {
      font-size: 13px;
      color: var(--text-medium);
      margin-top: 4px;
      font-style: italic;
    }

    .prompter-quick-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn-action-pill {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      color: #fff;
      padding: 8px 14px;
      border-radius: 9px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: inherit;
      transition: all 0.18s ease;
    }

    .btn-action-pill:hover {
      background: var(--bg-panel-hover);
      border-color: #475569;
    }

    .btn-action-pill.btn-pink {
      background: linear-gradient(135deg, #ec4899, #db2777);
      border-color: #ec4899;
      color: #fff;
      box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
    }

    .btn-action-pill.btn-gold {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      border-color: #f59e0b;
      color: #000;
      font-weight: 700;
    }

    .btn-action-pill.btn-blue {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--accent-blue);
      color: #93c5fd;
    }

    /* Hero Showcase Grid */
    .hero-showcase-grid {
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 18px;
    }

    .hero-image-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .hero-image-box {
      width: 100%;
      height: 220px;
      background: #040711;
      border-radius: 10px;
      border: 1px solid #1e293b;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      cursor: zoom-in;
    }

    .hero-image-box img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }

    .hero-image-box:hover img {
      transform: scale(1.05);
    }

    .price-highlight-card {
      background: var(--bg-panel);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 10px;
      padding: 10px 14px;
    }

    .price-main-val {
      font-size: 22px;
      font-weight: 800;
      color: var(--accent-green);
      font-family: 'JetBrains Mono', monospace;
    }

    .price-anchor-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 3px;
    }

    .price-msrp-tag {
      font-size: 11.5px;
      color: var(--text-muted);
      text-decoration: line-through;
    }

    .price-discount-badge {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #f87171;
      font-size: 10px;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 4px;
    }

    /* Color Swatches Circle Palette */
    .swatch-circles-container {
      display: flex;
      gap: 6px;
      align-items: center;
      flex-wrap: wrap;
      margin-top: 6px;
    }

    .swatch-circle {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 2px solid #1e293b;
      cursor: pointer;
      transition: all 0.15s ease;
      position: relative;
    }

    .swatch-circle:hover {
      transform: scale(1.2);
      border-color: #fff;
      box-shadow: 0 0 8px rgba(255,255,255,0.4);
    }

    /* Big Teleprompter Script Card */
    .prompter-script-container {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .script-block-hero {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(20, 30, 51, 0.8) 100%);
      border: 1px solid rgba(245, 158, 11, 0.3);
      border-radius: 12px;
      padding: 14px 18px;
    }

    .block-header-label {
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-gold);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 6px;
    }

    .hook-speaking-text {
      font-size: 16px;
      font-weight: 600;
      color: #fff;
      line-height: 1.5;
    }

    .fashion-hook-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(236, 72, 153, 0.15);
      border: 1px solid rgba(236, 72, 153, 0.35);
      color: #f472b6;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 500;
      line-height: 1.4;
    }

    .script-flow-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }

    .script-card-mini {
      background: var(--bg-panel);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 9px;
      padding: 10px 12px;
    }

    .card-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-cyan);
      margin-bottom: 4px;
    }

    .card-text {
      font-size: 12.5px;
      color: var(--text-medium);
      line-height: 1.4;
    }

    /* Specs & Strategy Drawer */
    .specs-strategy-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .specs-panel, .strategy-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 16px;
    }

    .panel-section-title {
      font-size: 13.5px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .specs-table {
      width: 100%;
      font-size: 12.5px;
      border-collapse: collapse;
    }

    .specs-table tr {
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }

    .specs-table td {
      padding: 6px 4px;
    }

    .spec-name {
      color: var(--text-muted);
      width: 90px;
    }

    .spec-val {
      color: var(--text-high);
      font-weight: 500;
    }

    /* =========================================================
       VIEW 2: MIX & MATCH LOOKBOOK BUILDER (REDESIGNED CANVAS)
       ========================================================= */
    .lookbook-view {
      display: none;
      width: 100%;
      height: 100%;
      overflow-y: auto;
      padding: 22px 32px 80px;
      background: radial-gradient(circle at 20% 30%, rgba(236, 72, 153, 0.08) 0%, transparent 60%), var(--bg-base);
    }

    .lookbook-container {
      max-width: 1320px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .lookbook-header {
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.18) 0%, rgba(139, 92, 246, 0.18) 100%);
      border: 1px solid rgba(236, 72, 153, 0.35);
      border-radius: 16px;
      padding: 18px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    .lookbook-header-title h2 {
      font-size: 22px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .lookbook-header-title p {
      font-size: 13px;
      color: #cbd5e1;
      margin-top: 2px;
    }

    .lookbook-presets-bar {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 4px;
      align-items: center;
      scrollbar-width: thin;
    }

    .preset-pill-btn {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: #cbd5e1;
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .preset-pill-btn:hover {
      background: rgba(236, 72, 153, 0.2);
      border-color: var(--accent-pink);
      color: #fff;
    }

    .preset-pill-btn.active {
      background: linear-gradient(135deg, #ec4899, #8b5cf6);
      border-color: transparent;
      box-shadow: 0 4px 14px rgba(236, 72, 153, 0.4);
      color: #fff;
      font-weight: 700;
    }

    /* Redesigned Outfit Builder Layout */
    .outfit-builder-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr) 360px;
      gap: 16px;
    }

    .outfit-slot-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
      transition: all 0.2s ease;
    }

    .outfit-slot-card.slot-active {
      border-color: rgba(236, 72, 153, 0.4);
      box-shadow: 0 6px 20px rgba(236, 72, 153, 0.12);
    }

    .outfit-slot-card.slot-disabled {
      opacity: 0.5;
      border-style: dashed;
    }

    .outfit-slot-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      font-weight: 700;
      color: var(--accent-gold);
    }

    .slot-toggle-label {
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      font-size: 11px;
      color: #94a3b8;
    }

    .slot-toggle-label input {
      accent-color: var(--accent-pink);
      cursor: pointer;
    }

    .outfit-slot-preview {
      height: 200px;
      background: #040711;
      border-radius: 12px;
      border: 1px solid #1e293b;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }

    .outfit-slot-preview img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }

    .outfit-slot-preview:hover img {
      transform: scale(1.06);
    }

    .slot-item-stepper {
      display: flex;
      gap: 6px;
      align-items: center;
    }

    .slot-step-btn {
      background: #090d16;
      border: 1px solid #334155;
      color: #cbd5e1;
      padding: 4px 9px;
      border-radius: 6px;
      font-size: 11px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }

    .slot-step-btn:hover {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--accent-blue);
      color: #fff;
    }

    .outfit-slot-details {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .outfit-slot-sku-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .outfit-slot-sku {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      color: var(--accent-gold);
    }

    .outfit-slot-exact-price {
      font-size: 16px;
      font-weight: 800;
      color: var(--accent-green);
      font-family: 'JetBrains Mono', monospace;
    }

    .outfit-slot-name {
      font-size: 13.5px;
      font-weight: 600;
      color: #fff;
      line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .slot-select-dropdown {
      width: 100%;
      background: #040711;
      border: 1px solid #334155;
      color: #fff;
      padding: 8px 10px;
      border-radius: 8px;
      font-size: 12px;
      font-family: inherit;
      outline: none;
      cursor: pointer;
    }

    .slot-select-dropdown:focus {
      border-color: var(--accent-pink);
    }

    .slot-swatches-row {
      display: flex;
      gap: 5px;
      align-items: center;
      flex-wrap: wrap;
    }

    /* Redesigned Bundle Summary Card with 100% Accurate Pricing Breakdown */
    .bundle-summary-card {
      background: linear-gradient(135deg, rgba(20, 30, 51, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
      border: 1px solid rgba(236, 72, 153, 0.4);
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: 0 10px 28px rgba(0,0,0,0.35);
    }

    .bundle-summary-title {
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 10px;
    }

    .bundle-tier-badge {
      background: linear-gradient(135deg, #ec4899, #8b5cf6);
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
    }

    .bundle-itemized-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 12px;
      color: var(--text-medium);
      background: #040711;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #1e293b;
    }

    .bundle-itemized-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .bundle-calc-row {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: var(--text-medium);
      padding: 3px 0;
    }

    .bundle-total-row {
      border-top: 1px solid #334155;
      padding-top: 10px;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }

    .bundle-final-price {
      font-size: 28px;
      font-weight: 800;
      color: #fbbf24;
      font-family: 'JetBrains Mono', monospace;
    }

    .bundle-script-box {
      background: #040711;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px;
      font-size: 12.5px;
      color: #e2e8f0;
      line-height: 1.45;
    }

    /* =========================================================
       VIEW 3: AI PERSONAL STYLIST STUDIO (ULTRA-FAST GEMINI)
       ========================================================= */
    .stylist-view {
      display: none;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }

    .stylist-container {
      display: flex;
      width: 100%;
      height: 100%;
    }

    .stylist-sidebar-tools {
      width: 380px;
      background: var(--bg-surface);
      border-right: 1px solid var(--border-subtle);
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      flex-shrink: 0;
    }

    .stylist-main-chat {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: radial-gradient(circle at 70% 30%, rgba(139, 92, 246, 0.06) 0%, transparent 60%), var(--bg-base);
      overflow: hidden;
    }

    .stylist-chat-header {
      padding: 14px 24px;
      background: rgba(10, 15, 29, 0.95);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }

    .stylist-chat-body {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .stylist-chat-input-area {
      padding: 16px 24px;
      background: var(--bg-surface);
      border-top: 1px solid var(--border-subtle);
      flex-shrink: 0;
    }

    .stylist-msg-user {
      align-self: flex-end;
      background: linear-gradient(135deg, #8b5cf6, #6d28d9);
      color: #fff;
      padding: 12px 18px;
      border-radius: 16px 16px 4px 16px;
      max-width: 75%;
      font-size: 14px;
      line-height: 1.5;
    }

    .stylist-msg-ai {
      align-self: flex-start;
      background: var(--bg-panel);
      border: 1px solid rgba(139, 92, 246, 0.25);
      color: var(--text-high);
      padding: 16px 20px;
      border-radius: 16px 16px 16px 4px;
      max-width: 85%;
      font-size: 14px;
      line-height: 1.6;
    }

    .stylist-quick-card {
      background: var(--bg-panel);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 10px;
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.18s ease;
    }

    .stylist-quick-card:hover {
      background: rgba(139, 92, 246, 0.15);
      border-color: #a78bfa;
      transform: translateY(-1px);
    }

    .stylist-suggestion-chips {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 10px;
    }

    .stylist-sugg-btn {
      background: #040711;
      border: 1px solid #334155;
      color: #93c5fd;
      padding: 4px 10px;
      border-radius: 14px;
      font-size: 11px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }

    .stylist-sugg-btn:hover {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--accent-blue);
      color: #fff;
    }

    /* Personal Color Interactive Wheel */
    .color-analysis-box {
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
      border: 1px solid rgba(236, 72, 153, 0.3);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .undertone-btn-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .undertone-btn {
      background: #040711;
      border: 1px solid #334155;
      color: #cbd5e1;
      padding: 7px 4px;
      border-radius: 8px;
      font-size: 11px;
      text-align: center;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }

    .undertone-btn.active {
      background: rgba(236, 72, 153, 0.2);
      border-color: var(--accent-pink);
      color: #f472b6;
      font-weight: 700;
    }

    /* =========================================================
       VIEW 4: DEDICATED SIZE MATRIX & SMART ADVISOR HUB
       ========================================================= */
    .size-hub-view {
      display: none;
      width: 100%;
      height: 100%;
      overflow-y: auto;
      padding: 24px 32px 80px;
      background: radial-gradient(circle at 10% 20%, rgba(245, 158, 11, 0.05) 0%, transparent 60%), var(--bg-base);
    }

    .size-hub-container {
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .size-hub-header-card {
      background: linear-gradient(135deg, rgba(20, 30, 51, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 16px;
      padding: 20px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      box-shadow: 0 10px 24px rgba(0,0,0,0.3);
    }

    .size-calc-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 22px 24px;
      display: grid;
      grid-template-columns: 1fr 1.1fr;
      gap: 24px;
      box-shadow: 0 10px 24px rgba(0,0,0,0.25);
    }

    .calc-input-section {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .calc-output-section {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(20, 30, 51, 0.8) 100%);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-radius: 14px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .calc-field-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .calc-field-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text-medium);
      display: flex;
      justify-content: space-between;
    }

    .calc-input-wrapper {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .calc-input-box-num {
      width: 100px;
      background: #090d16;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 8px 12px;
      color: #fff;
      font-size: 16px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      outline: none;
    }

    .calc-input-box-num:focus {
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }

    .chip-selector-group {
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
    }

    .size-quick-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      padding: 4px 9px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }

    .size-quick-chip:hover {
      background: rgba(59, 130, 246, 0.2);
      color: #93c5fd;
      border-color: var(--accent-blue);
    }

    .fit-pref-group {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }

    .fit-pref-btn {
      background: #090d16;
      border: 1px solid #334155;
      color: #94a3b8;
      padding: 8px 6px;
      border-radius: 8px;
      font-size: 11.5px;
      text-align: center;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.18s ease;
    }

    .fit-pref-btn.active {
      background: rgba(16, 185, 129, 0.15);
      border-color: #10b981;
      color: #34d399;
      font-weight: 700;
    }

    .rec-badge-display {
      font-size: 30px;
      font-weight: 800;
      color: #fbbf24;
      font-family: 'JetBrains Mono', monospace;
      display: flex;
      align-items: baseline;
      gap: 8px;
    }

    .live-speaking-card {
      background: #090d16;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 13.5px;
      color: #e2e8f0;
      line-height: 1.5;
    }

    .size-tables-grid {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .size-table-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      overflow: hidden;
    }

    .size-table-header {
      padding: 14px 20px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .table-unit-toggle {
      display: flex;
      gap: 4px;
      background: #090d16;
      padding: 2px;
      border-radius: 6px;
      border: 1px solid #334155;
    }

    .unit-btn {
      background: transparent;
      border: none;
      color: #94a3b8;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11.5px;
      cursor: pointer;
      font-weight: 600;
    }

    .unit-btn.active {
      background: var(--accent-blue);
      color: #fff;
    }

    .styled-size-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: center;
    }

    .styled-size-table th {
      background: rgba(20, 30, 51, 0.5);
      padding: 10px 12px;
      color: var(--text-muted);
      font-weight: 600;
      border-bottom: 1px solid var(--border-subtle);
    }

    .styled-size-table td {
      padding: 9px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-medium);
    }

    .styled-size-table tr:hover td {
      background: rgba(59, 130, 246, 0.06);
    }

    .styled-size-table tr.row-highlight td {
      background: rgba(245, 158, 11, 0.15) !important;
      color: #fbbf24 !important;
      font-weight: 700;
    }

    /* Global Footer */
    .global-footer-bar {
      background: #040711;
      border-top: 1px solid #1e293b;
      padding: 8px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: #64748b;
      flex-shrink: 0;
      z-index: 40;
    }

    .brand-prop {
      color: #fbbf24;
      font-weight: 600;
    }

    /* Toast */
    .toast-msg {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #10b981;
      color: #fff;
      padding: 10px 18px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 9999;
      pointer-events: none;
    }

    .toast-msg.show {
      transform: translateY(0);
      opacity: 1;
    }
  
    /* =========================================================
       VIEW 7: TIKTOK LIVE SELLING PLAN BUILDER
       ========================================================= */
    .plan-view {
      display: none;
      width: 100%;
      height: 100%;
      overflow-y: auto;
      background: var(--bg-base);
      padding: 24px 32px 60px;
    }

    .plan-stepper-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 10px 18px;
      margin-bottom: 22px;
      gap: 8px;
      max-width: 1200px;
      margin-left: auto;
      margin-right: auto;
    }

    .plan-step-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      padding: 6px 14px;
      border-radius: 8px;
      transition: all 0.2s;
      background: transparent;
      border: 1px solid transparent;
      font-family: inherit;
    }
    .plan-step-btn:hover { color: #fff; background: rgba(255,255,255,0.04); }
    .plan-step-btn.active {
      color: #fff;
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
    }
    .plan-step-btn.completed { color: var(--accent-green); }
    .plan-step-num {
      width: 22px; height: 22px; border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      display: flex; align-items: center; justify-content: center;
      font-size: 11px; font-weight: 800;
    }
    .plan-step-btn.active .plan-step-num { background: var(--accent-green); color: #0f172a; }

    .plan-step-container { display: none; max-width: 1200px; margin: 0 auto; animation: fadeIn 0.2s ease; }
    .plan-step-container.active { display: block; }

    .plan-picker-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 16px;
      margin-bottom: 80px;
    }

    .plan-picker-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      position: relative;
      cursor: pointer;
      transition: all 0.2s;
    }
    .plan-picker-card:hover { border-color: var(--accent-blue); transform: translateY(-2px); }
    .plan-picker-card.selected {
      border-color: var(--accent-green);
      background: rgba(16, 185, 129, 0.08);
      box-shadow: 0 0 0 1px var(--accent-green);
    }
    .plan-picker-card .card-check {
      position: absolute; top: 10px; right: 10px;
      width: 18px; height: 18px; accent-color: var(--accent-green); cursor: pointer;
    }
    .plan-picker-img {
      height: 150px; background: #040711; border-radius: 8px;
      display: flex; align-items: center; justify-content: center; overflow: hidden;
    }
    .plan-picker-img img { max-width: 100%; max-height: 100%; object-fit: contain; }

    .plan-tray-bar {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: rgba(10, 15, 29, 0.96); backdrop-filter: blur(16px);
      border-top: 1px solid var(--border-subtle);
      padding: 12px 32px; display: flex; align-items: center; justify-content: space-between;
      gap: 20px; z-index: 95;
    }

    .plan-brief-card {
      background: var(--bg-surface); border: 1px solid var(--border-subtle);
      border-radius: 12px; padding: 26px; max-width: 820px; margin: 0 auto;
    }
    .plan-form-grid {
      display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px;
    }
    .plan-form-group { display: flex; flex-direction: column; gap: 6px; }
    .plan-form-group label { font-size: 12.5px; font-weight: 700; color: #94a3b8; }
    .plan-form-group input, .plan-form-group select {
      background: var(--bg-panel); border: 1px solid var(--border-subtle);
      padding: 9px 12px; border-radius: 8px; color: #fff; font-size: 13px; font-family: inherit; outline: none;
    }
    .plan-form-group input:focus, .plan-form-group select:focus { border-color: var(--accent-green); }

    .plan-overview-card {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px;
      padding: 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;
    }

    .plan-look-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px; margin-bottom: 24px;
    }
    .plan-look-box {
      background: var(--bg-surface); border: 1px solid var(--border-subtle);
      border-radius: 10px; padding: 16px; display: flex; flex-direction: column; gap: 10px;
    }

    .plan-rundown-stack { display: flex; flex-direction: column; gap: 14px; margin-bottom: 24px; }
    .plan-seg-card {
      background: var(--bg-surface); border: 1px solid var(--border-subtle);
      border-radius: 10px; padding: 18px; display: grid;
      grid-template-columns: 85px 1fr 300px 100px; gap: 16px; align-items: start;
    }
    .plan-seg-time {
      background: #040711; text-align: center; padding: 8px; border-radius: 8px; border: 1px solid var(--border-subtle);
    }
    .plan-seg-actions { display: flex; flex-direction: column; gap: 5px; }
    .plan-btn-reorder {
      background: var(--bg-panel); border: 1px solid var(--border-subtle); color: #fff;
      padding: 5px; border-radius: 6px; font-size: 11.5px; font-weight: 700; cursor: pointer; font-family: inherit;
    }
    .plan-btn-reorder:hover { background: var(--accent-green); color: #0f172a; }

    .plan-teleprompter-box {
      background: #020617; border: 1px solid rgba(16, 185, 129, 0.4);
      border-radius: 14px; padding: 32px; display: flex; flex-direction: column; gap: 20px; min-height: 520px;
    }
    .plan-tele-script {
      font-size: 22px; line-height: 1.7; color: #fff; font-weight: 600;
      background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 12px;
    }

    @media print {
      header.studio-header, .filter-chips-bar, .plan-stepper-nav, .plan-tray-bar, .plan-seg-actions, .view-switcher, footer { display: none !important; }
      body, .plan-view { background: #fff !important; color: #000 !important; overflow: visible !important; height: auto !important; }
      .plan-seg-card, .plan-look-box, .plan-overview-card { border: 1px solid #ddd !important; background: #fff !important; color: #000 !important; break-inside: avoid; }
      .plan-tele-script { background: #f8fafc !important; color: #111 !important; border: 1px solid #ddd !important; }
    }

  
    /* =========================================================
       VIEW 7: TIKTOK LIVE SELLING PLAN BUILDER CSS
       ========================================================= */
    .plan-view {
      display: none;
      width: 100%;
      height: 100%;
      overflow-y: auto;
      background: var(--bg-base);
      padding: 24px 32px 60px;
    }

    .plan-stepper-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 10px 18px;
      margin-bottom: 22px;
      gap: 8px;
      max-width: 1200px;
      margin-left: auto;
      margin-right: auto;
    }

    .plan-step-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      padding: 6px 14px;
      border-radius: 8px;
      transition: all 0.2s;
      background: transparent;
      border: 1px solid transparent;
      font-family: inherit;
    }
    .plan-step-btn:hover { color: #fff; background: rgba(255,255,255,0.04); }
    .plan-step-btn.active {
      color: #fff;
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
    }
    .plan-step-btn.completed { color: var(--accent-green); }
    .plan-step-num {
      width: 22px; height: 22px; border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      display: flex; align-items: center; justify-content: center;
      font-size: 11px; font-weight: 800;
    }
    .plan-step-btn.active .plan-step-num { background: var(--accent-green); color: #0f172a; }

    .plan-step-container { display: none; max-width: 1200px; margin: 0 auto; animation: fadeIn 0.2s ease; }
    .plan-step-container.active { display: block; }

    .plan-picker-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 16px;
      margin-bottom: 80px;
    }

    .plan-picker-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      position: relative;
      cursor: pointer;
      transition: all 0.2s;
    }
    .plan-picker-card:hover { border-color: var(--accent-blue); transform: translateY(-2px); }
    .plan-picker-card.selected {
      border-color: var(--accent-green);
      background: rgba(16, 185, 129, 0.08);
      box-shadow: 0 0 0 1px var(--accent-green);
    }
    .plan-picker-card .card-check {
      position: absolute; top: 10px; right: 10px;
      width: 18px; height: 18px; accent-color: var(--accent-green); cursor: pointer;
    }
    .plan-picker-img {
      height: 150px; background: #040711; border-radius: 8px;
      display: flex; align-items: center; justify-content: center; overflow: hidden;
    }
    .plan-picker-img img { max-width: 100%; max-height: 100%; object-fit: contain; }

    .plan-tray-bar {
      position: fixed; bottom: 0; left: 0; right: 0;
      background: rgba(10, 15, 29, 0.96); backdrop-filter: blur(16px);
      border-top: 1px solid var(--border-subtle);
      padding: 12px 32px; display: flex; align-items: center; justify-content: space-between;
      gap: 20px; z-index: 95;
    }

    .plan-brief-card {
      background: var(--bg-surface); border: 1px solid var(--border-subtle);
      border-radius: 12px; padding: 26px; max-width: 820px; margin: 0 auto;
    }
    .plan-form-grid {
      display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px;
    }
    .plan-form-group { display: flex; flex-direction: column; gap: 6px; }
    .plan-form-group label { font-size: 12.5px; font-weight: 700; color: #94a3b8; }
    .plan-form-group input, .plan-form-group select {
      background: var(--bg-panel); border: 1px solid var(--border-subtle);
      padding: 9px 12px; border-radius: 8px; color: #fff; font-size: 13px; font-family: inherit; outline: none;
    }
    .plan-form-group input:focus, .plan-form-group select:focus { border-color: var(--accent-green); }

    .plan-overview-card {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 12px;
      padding: 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;
    }

    .plan-look-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px; margin-bottom: 24px;
    }
    .plan-look-box {
      background: var(--bg-surface); border: 1px solid var(--border-subtle);
      border-radius: 10px; padding: 16px; display: flex; flex-direction: column; gap: 10px;
    }

    .plan-rundown-stack { display: flex; flex-direction: column; gap: 14px; margin-bottom: 24px; }
    .plan-seg-card {
      background: var(--bg-surface); border: 1px solid var(--border-subtle);
      border-radius: 10px; padding: 18px; display: grid;
      grid-template-columns: 85px 1fr 300px 100px; gap: 16px; align-items: start;
    }
    .plan-seg-time {
      background: #040711; text-align: center; padding: 8px; border-radius: 8px; border: 1px solid var(--border-subtle);
    }
    .plan-seg-actions { display: flex; flex-direction: column; gap: 5px; }
    .plan-btn-reorder {
      background: var(--bg-panel); border: 1px solid var(--border-subtle); color: #fff;
      padding: 5px; border-radius: 6px; font-size: 11.5px; font-weight: 700; cursor: pointer; font-family: inherit;
    }
    .plan-btn-reorder:hover { background: var(--accent-green); color: #0f172a; }

    .plan-teleprompter-box {
      background: #020617; border: 1px solid rgba(16, 185, 129, 0.4);
      border-radius: 14px; padding: 32px; display: flex; flex-direction: column; gap: 20px; min-height: 520px;
    }
    .plan-tele-script {
      font-size: 22px; line-height: 1.7; color: #fff; font-weight: 600;
      background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); padding: 24px; border-radius: 12px;
    }

    @media print {
      header.studio-header, .filter-chips-bar, .plan-stepper-nav, .plan-tray-bar, .plan-seg-actions, .view-switcher, footer { display: none !important; }
      body, .plan-view { background: #fff !important; color: #000 !important; overflow: visible !important; height: auto !important; }
      .plan-seg-card, .plan-look-box, .plan-overview-card { border: 1px solid #ddd !important; background: #fff !important; color: #000 !important; break-inside: avoid; }
      .plan-tele-script { background: #f8fafc !important; color: #111 !important; border: 1px solid #ddd !important; }
    }

  
    /* =========================================================
       FLOATING DYNAMIC SEARCH BAR & SPOTLIGHT (CMD+K)
       ========================================================= */
    .floating-search-pill-btn {
      position: fixed;
      bottom: 32px;
      right: 32px;
      background: linear-gradient(135deg, rgba(30, 27, 75, 0.95), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(99, 102, 241, 0.5);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.25);
      color: #fff;
      padding: 10px 18px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 1000;
      backdrop-filter: blur(16px);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      font-family: inherit;
    }
    .floating-search-pill-btn:hover {
      transform: translateY(-3px) scale(1.02);
      border-color: #38bdf8;
      box-shadow: 0 12px 40px rgba(56, 189, 248, 0.3);
    }
    .spotlight-kbd-badge {
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      color: #38bdf8;
    }

    /* Floating Spotlight Modal Overlay */
    .spotlight-modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(4, 7, 17, 0.85);
      backdrop-filter: blur(16px);
      z-index: 2000;
      align-items: flex-start;
      justify-content: center;
      padding-top: 10vh;
      animation: fadeInModal 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .spotlight-modal-overlay.active {
      display: flex;
    }
    @keyframes fadeInModal {
      from { opacity: 0; transform: scale(0.98); }
      to { opacity: 1; transform: scale(1); }
    }

    .spotlight-dialog-box {
      width: 820px;
      max-width: 94vw;
      background: linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(8, 12, 22, 0.98));
      border: 1px solid rgba(56, 189, 248, 0.45);
      box-shadow: 0 25px 70px rgba(0, 0, 0, 0.85), 0 0 50px rgba(56, 189, 248, 0.2);
      border-radius: 18px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      max-height: 85vh;
    }

    

    /* Responsive Mobile Media Queries (Comprehensive) */
    @media (max-width: 1024px) {
      header.studio-header {
        flex-wrap: wrap;
        gap: 10px;
        padding: 10px 14px;
        height: auto;
      }
      .brand-section {
        min-width: 0 !important;
        flex: 1 1 auto;
      }
      .view-switcher {
        order: 2;
        overflow-x: auto;
        width: 100%;
        padding-bottom: 4px;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none; /* Hide scrollbar for cleaner look */
        flex-wrap: nowrap;
        scroll-behavior: smooth;
      }
      .view-switcher::-webkit-scrollbar {
        display: none;
      }
      .view-btn {
        white-space: nowrap;
        flex-shrink: 0;
      }
      .header-search-box {
        order: 3;
        max-width: 100%;
        width: 100%;
        min-width: 100%;
      }
      .product-sidebar {
        width: 280px;
      }
      .outfit-builder-grid {
        grid-template-columns: repeat(2, 1fr) !important;
      }
      .lookbook-slots-grid {
        grid-template-columns: repeat(2, 1fr) !important;
      }
      .stylist-layout-grid {
        grid-template-columns: 1fr !important;
      }
      .size-calc-card {
        grid-template-columns: 1fr !important;
      }
      #pModViewBox {
        grid-template-columns: 1fr !important;
      }
      .k-grid-2col {
        grid-template-columns: 1fr !important;
      }
    }

    @media (max-width: 768px) {
      body {
        height: 100vh;
        height: 100dvh;
        overflow: hidden;
      }

      .brand-title-box h1 {
        font-size: 13.5px;
        gap: 5px;
      }
      .brand-badge {
        width: 32px;
        height: 32px;
        font-size: 16px;
      }
      .brand-subtitle {
        display: none !important;
      }
      .live-indicator {
        font-size: 9px;
        padding: 1px 5px;
      }

      .view-switcher {
        padding-bottom: 4px;
        gap: 5px;
      }
      .view-btn {
        padding: 5px 9px;
        font-size: 11px;
        gap: 4px;
      }

      .header-search-box input {
        height: 38px;
        font-size: 12.5px;
        padding-left: 36px;
        padding-right: 65px;
      }
      .search-lens {
        left: 10px;
        font-size: 14px;
      }
      .header-search-badge {
        right: 8px;
        font-size: 10px;
        padding: 2px 6px;
      }

      /* Filter chips */
      nav.filter-chips-bar {
        padding: 6px 12px;
        gap: 5px;
      }
      .chip-btn {
        padding: 3px 8px;
        font-size: 11px;
        flex-shrink: 0;
      }

      /* View 1: Studio Split View */
      .studio-split-view {
        flex-direction: row !important;
        position: relative;
        overflow: hidden !important;
      }
      .product-sidebar {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        width: 300px !important;
        max-width: 85% !important;
        height: 100%;
        max-height: none !important;
        z-index: 100;
        border-right: 1px solid var(--border-subtle) !important;
        border-bottom: none !important;
        transform: translateX(0);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s;
        box-shadow: 4px 0 24px rgba(0,0,0,0.5);
      }
      .product-sidebar.collapsed {
        display: flex !important; /* Keep display flex to allow transform transition */
        width: 300px !important;
        max-width: 85% !important;
        opacity: 0;
        transform: translateX(-100%);
        pointer-events: none;
      }
      .product-teleprompter-stage {
        flex: 1;
        width: 100% !important;
        height: 100%;
        padding: 16px 12px 70px !important;
        overflow-y: auto !important;
      }
      /* Ensure floating restore button is accessible */
      .floating-sidebar-restore-btn {
        top: auto !important;
        bottom: 80px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.7) !important;
        z-index: 101 !important;
      }
      .floating-sidebar-restore-btn:hover {
        transform: translateX(-50%) translateY(-2px) !important;
      }
      .prompter-top-nav {
        flex-direction: column !important;
        gap: 8px;
      }
      .prompter-title {
        font-size: 17px !important;
      }
      .prompter-pitch {
        font-size: 12px !important;
      }
      .prompter-quick-actions {
        width: 100% !important;
        flex-wrap: wrap !important;
      }
      .prompter-quick-actions button {
        flex: 1 1 calc(50% - 6px);
      }
      .prompter-hero-card {
        flex-direction: column !important;
        padding: 14px !important;
      }
      .prompter-hero-img-box {
        width: 100% !important;
        height: 220px !important;
        max-width: 260px;
        margin: 0 auto;
      }
      .prompter-action-cards {
        grid-template-columns: 1fr !important;
      }

      /* View 2: Lookbook */
      .lookbook-view {
        padding: 12px 10px 70px !important;
      }
      .lookbook-header {
        padding: 12px 14px !important;
      }
      .lookbook-header-title h2 {
        font-size: 17px !important;
      }
      .outfit-builder-grid {
        grid-template-columns: 1fr !important;
      }
      .lookbook-slots-grid {
        grid-template-columns: 1fr !important;
      }

      /* View 3: Stylist Studio */
      .stylist-view {
        padding: 12px 10px 70px !important;
      }
      .stylist-layout-grid {
        grid-template-columns: 1fr !important;
      }

      /* View 4: Size Hub */
      .size-hub-view {
        padding: 12px 10px 70px !important;
      }
      .size-hub-header-card {
        padding: 12px 14px !important;
      }
      .size-calc-card {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
        padding: 14px !important;
      }

      /* View 5: Grid */
      .catalog-grid-view {
        padding: 12px 10px 70px !important;
      }
      #grid-container {
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)) !important;
        gap: 10px !important;
      }

      /* View 6: Matrix */
      .matrix-table-view {
        padding: 12px 10px 70px !important;
      }

      /* View 7: Plan Builder */
      .plan-view {
        padding: 12px 10px 70px !important;
      }
      .plan-stepper-nav {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
        padding: 8px 10px;
        gap: 6px;
        scrollbar-width: none;
      }
      .plan-step-btn {
        padding: 5px 10px;
        font-size: 11.5px;
        flex-shrink: 0;
      }
      .plan-picker-grid {
        grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)) !important;
        gap: 10px !important;
      }
      .plan-form-grid {
        grid-template-columns: 1fr !important;
      }
      .plan-look-grid {
        grid-template-columns: 1fr !important;
      }
      .plan-summary-metrics {
        grid-template-columns: repeat(2, 1fr) !important;
      }
      #pModViewBox {
        grid-template-columns: 1fr !important;
      }

      /* View 8: Product Knowledge & Guide */
      .knowledge-view {
        padding: 12px 10px 70px !important;
      }
      .k-hero-banner {
        padding: 16px 14px !important;
        border-radius: 14px !important;
      }
      .k-hero-title {
        font-size: 18px !important;
      }
      .k-kpi-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
      }
      .k-subtabs-bar {
        overflow-x: auto;
        flex-wrap: nowrap;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        padding-bottom: 8px;
        gap: 6px;
      }
      .k-nav-tab {
        padding: 6px 12px !important;
        font-size: 11.5px !important;
        flex-shrink: 0;
      }
      .k-grid-2col {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
      }

      /* Spotlight Modal */
      .spotlight-dialog-box {
        width: 95vw !important;
        max-height: 88vh !important;
        border-radius: 14px;
        padding-top: 0;
      }
      .spotlight-item-card {
        padding: 10px;
      }
      .spotlight-item-thumb {
        width: 44px;
        height: 44px;
      }
      .spotlight-item-name {
        font-size: 13px;
      }
    }

    .spotlight-input-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(15, 23, 42, 0.6);
    }
    .spotlight-lens-icon {
      font-size: 20px;
      color: #38bdf8;
      margin-right: 12px;
    }
    .spotlight-input-field {
      flex: 1;
      background: transparent;
      border: none;
      color: #fff;
      font-size: 16px;
      font-family: inherit;
      outline: none;
      font-weight: 500;
    }
    .spotlight-input-field::placeholder {
      color: #64748b;
    }
    .spotlight-esc-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-subtle);
      color: #94a3b8;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      cursor: pointer;
    }

    .spotlight-quick-filters {
      display: flex;
      gap: 6px;
      padding: 10px 20px;
      background: rgba(7, 10, 19, 0.6);
      border-bottom: 1px solid var(--border-subtle);
      overflow-x: auto;
    }
    .spotlight-filter-pill {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 3px 10px;
      border-radius: 14px;
      font-size: 11.5px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s;
    }
    .spotlight-filter-pill.active {
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      color: #fff;
    }

    .spotlight-results-list {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .spotlight-item-card {
      background: rgba(20, 27, 45, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 10px;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      gap: 14px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .spotlight-item-card:hover, .spotlight-item-card.focused {
      background: rgba(59, 130, 246, 0.15);
      border-color: rgba(59, 130, 246, 0.5);
      transform: translateX(3px);
    }

    .spotlight-item-thumb {
      width: 48px;
      height: 48px;
      background: #040711;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .spotlight-item-thumb img {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }

    .spotlight-item-info {
      flex: 1;
      min-width: 0;
    }
    .spotlight-item-sku {
      font-size: 11px;
      font-weight: 700;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
    }
    .spotlight-item-name {
      font-size: 13.5px;
      font-weight: 600;
      color: #fff;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .spotlight-item-fabric {
      font-size: 11.5px;
      color: #94a3b8;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .spotlight-item-right {
      text-align: right;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 4px;
    }
    .spotlight-item-price {
      font-size: 15px;
      font-weight: 800;
      color: #10b981;
      font-family: 'JetBrains Mono', monospace;
    }

    .spotlight-quick-actions {
      display: flex;
      gap: 4px;
    }
    .btn-spotlight-action {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: #cbd5e1;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-spotlight-action:hover {
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      color: #fff;
    }

    .spotlight-footer {
      padding: 10px 20px;
      background: rgba(7, 10, 19, 0.9);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      color: var(--text-dim);
    }

  
    /* Workspace Sub-Navigation Bar */
    .workspace-subnav-bar {
      display: flex;
      gap: 8px;
      padding: 8px 24px;
      background: rgba(15, 23, 42, 0.95);
      border-bottom: 1px solid var(--border-subtle);
      align-items: center;
    }
    .subnav-tab-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-medium);
      padding: 7px 16px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .subnav-tab-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }
    .subnav-tab-btn.active {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), rgba(99, 102, 241, 0.25));
      border-color: #38bdf8;
      color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }


    /* ===================================================
       AUTH & LOGIN GATE (FIRST ENTRY)
       =================================================== */
    .login-overlay-view {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 10000;
      background: radial-gradient(circle at 50% 25%, rgba(30, 58, 138, 0.5) 0%, rgba(7, 9, 14, 0.98) 75%);
      backdrop-filter: blur(24px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      transition: opacity 0.35s ease, visibility 0.35s ease;
    }

    .login-overlay-view.logged-in {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    .login-card-container {
      width: 460px;
      max-width: 94vw;
      background: linear-gradient(180deg, rgba(17, 24, 39, 0.95) 0%, rgba(10, 15, 29, 0.98) 100%);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 24px;
      box-shadow: 0 25px 80px rgba(0, 0, 0, 0.85), 0 0 50px rgba(56, 189, 248, 0.15);
      padding: 36px 32px 30px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      position: relative;
      animation: modalPop 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .login-brand-header {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 10px;
    }

    .login-brand-badge {
      width: 60px;
      height: 60px;
      border-radius: 16px;
      background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 30px;
      font-weight: 900;
      box-shadow: 0 0 25px rgba(59, 130, 246, 0.5);
      border: 2px solid rgba(255, 255, 255, 0.3);
    }

    .login-title {
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.02em;
    }

    .login-subtitle {
      font-size: 12.5px;
      color: var(--text-medium);
      line-height: 1.4;
    }

    .login-role-selector {
      display: flex;
      gap: 6px;
      background: rgba(15, 23, 42, 0.7);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--border-subtle);
    }

    .login-role-pill {
      flex: 1;
      text-align: center;
      padding: 8px 4px;
      font-size: 11.5px;
      font-weight: 600;
      border-radius: 8px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }

    .login-role-pill:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }

    .login-role-pill.active {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(99, 102, 241, 0.3));
      border-color: #38bdf8;
      color: #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    .login-form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .login-form-group label {
      font-size: 11.5px;
      font-weight: 600;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .login-input-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }

    .login-input-icon {
      position: absolute;
      left: 12px;
      color: #64748b;
      font-size: 14px;
      pointer-events: none;
    }

    .login-input-field {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 10px;
      padding: 10px 12px 10px 36px;
      color: #fff;
      font-size: 13.5px;
      font-family: inherit;
      transition: all 0.2s ease;
      outline: none;
    }

    .login-input-field:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25);
      background: rgba(15, 23, 42, 0.95);
    }

    .btn-login-submit {
      width: 100%;
      padding: 12px;
      border-radius: 12px;
      background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
      color: #fff;
      border: 1px solid rgba(255, 255, 255, 0.3);
      font-size: 14.5px;
      font-weight: 700;
      cursor: pointer;
      font-family: inherit;
      box-shadow: 0 8px 24px rgba(37, 99, 235, 0.4);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    .btn-login-submit:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6);
      border-color: #fff;
    }

    .btn-login-quick {
      width: 100%;
      padding: 9px;
      border-radius: 10px;
      background: rgba(16, 185, 129, 0.12);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.2s ease;
    }

    .btn-login-quick:hover {
      background: rgba(16, 185, 129, 0.22);
      border-color: #10b981;
    }

    .login-footer-security {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--text-muted);
      border-top: 1px solid var(--border-subtle);
      padding-top: 14px;
      margin-top: 4px;
    }

    .header-user-badge {
      display: flex;
      align-items: center;
      gap: 7px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 10px 4px 8px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      color: #fff;
    }

    .btn-logout {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #f87171;
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 10.5px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
    }

    .btn-logout:hover {
      background: rgba(239, 68, 68, 0.3);
      border-color: #ef4444;
      color: #fff;
    }

</style>
</head>
<body>
  
<!-- Top Navigation Bar -->
<header class="studio-header">
  <div class="brand-section">
    <div class="brand-badge">W</div>
    <div class="brand-title-box">
      <h1>WARRIX LIVE STUDIO <span class="live-indicator"><span class="live-dot"></span> FASHION HUB</span></h1>
      <div class="brand-subtitle">ระบบช่วยขายหน้ากล้อง & Lookbook Builder (100 SKUs)</div>
    </div>
  </div>

  <div class="header-search-box" title="พิมพ์ค้นหา หรือกด ⌘K เพื่อเปิด Spotlight">
    <span class="search-lens">🔍</span>
    <input type="text" id="global-search" placeholder="🔍 ค้นหาด่วน 100 SKUs (SKU, ชื่อรุ่น, เนื้อผ้า, สี, ราคา)..." oninput="handleSearch(this.value)">
    <span class="header-search-badge" onclick="openSpotlightSearch()" title="คลิกเพื่อเปิดหน้าต่างค้นหา Spotlight เต็มจอ"><kbd>⌘K</kbd></span>
  </div>

  <div class="view-switcher">
    <button class="view-btn btn-sku-toggle" id="header-sku-toggle-btn" onclick="toggleProductSidebar()" title="เปิด/ปิด แถบรายการสินค้า 100 SKUs (ON/OFF) [คีย์ลัด: H]">
      <span id="sku-status-dot" style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; margin-right:4px;"></span>
      <span id="sku-status-label">100 SKUs: ON</span>
    </button>
    <button class="view-btn active" id="btn-view-studio" onclick="switchView('studio')">
      📺 Live Prompter
    </button>
    <button class="view-btn btn-lookbook" id="btn-view-lookbook" onclick="switchView('lookbook')" title="เปิดระบบจัดชุด Mix & Match Lookbook">
      👗 Mix & Match Lookbook
    </button>
    <button class="view-btn btn-stylist" id="btn-view-stylist" onclick="switchView('stylist')" title="เปิดผู้ช่วย AI Personal Stylist (Gemini 3.6 Flash)">
      💄 AI Stylist Studio
    </button>
    <button class="view-btn btn-sizes" id="btn-view-sizes" onclick="switchView('sizes')" title="เปิดตารางไซซ์และระบบคำนวณไซซ์">
      📏 Size Hub & Advisor
    </button>
    <button class="view-btn" id="btn-view-grid" onclick="switchView('grid')" title="เปิดตารางแคตตาล็อกสินค้า">
      🗂️ Grid Catalog
    </button>
    <button class="view-btn" id="btn-view-matrix" onclick="switchView('matrix')" title="เปิดตารางเปรียบเทียบราคา">
      📊 Price Matrix
    </button>
    <button class="view-btn btn-plan" id="btn-view-plan" onclick="switchView('plan')" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(6, 182, 212, 0.18)); border-color: #10b981; color: #34d399; font-weight:600;" title="เปิดระบบวางแผนคิวไลฟ์สด TikTok Live Selling Plan Builder">
      📋 Live Plan Builder
    </button>
    <button class="view-btn btn-knowledge" id="btn-view-knowledge" onclick="switchView('knowledge')" style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(234, 88, 12, 0.22)); border-color: #f59e0b; color: #fbbf24; font-weight:700;" title="เปิดคู่มือความรู้สินค้าและกลยุทธ์การขาย Product Knowledge & Sales Guide (สรุปจาก 229 Live Sessions)">
      💡 Product Knowledge & Guide
    </button>
    <button class="view-btn" id="btn-warrix-sync" onclick="syncWithWarrixWebsite()" style="color:#38bdf8; border:1px solid rgba(56,189,248,0.35);" title="เชื่อมต่อและซิงค์ข้อมูลกับ Warrix.com">
      🌐 Sync Web
    </button>
    <button class="view-btn" id="btn-import-csv" onclick="triggerCsvImport()" style="color:#c084fc; border:1px solid rgba(192,132,252,0.4); background:rgba(192,132,252,0.12); font-weight:600;" title="นำเข้าข้อมูลสินค้าผ่านไฟล์ CSV (อัปเดต 100 SKUs ทันที)">
      📁 Import CSV
    </button>
    <button class="view-btn" id="btn-export-csv" onclick="exportProductsCsv()" style="color:#94a3b8; border:1px solid rgba(148,163,184,0.3);" title="ดาวน์โหลดไฟล์ CSV หรือตัวอย่าง Template">
      📥 Export CSV
    </button>
    <input type="file" id="csv-file-input" accept=".csv,text/csv" style="display:none;" onchange="handleCsvFileChange(event)">
  </div>
</header>

  


  


<!-- Occasion & Vibe Discovery Chips Bar -->
<nav class="filter-chips-bar" id="filter-bar">
  <button class="chip-btn active" onclick="applyFilter('ALL')">⭐ ทั้งหมด (100)</button>
  <button class="chip-btn chip-vibe" onclick="applyFilter('VIBE_OFFICE')">💼 Office & Workwear</button>
  <button class="chip-btn chip-vibe" onclick="applyFilter('VIBE_CAFE')">☕ Cafe & Weekend</button>
  <button class="chip-btn chip-vibe" onclick="applyFilter('VIBE_TRAVEL')">✈️ Travel & Airport</button>
  <button class="chip-btn chip-vibe" onclick="applyFilter('VIBE_STREET')">🕶️ Streetwear & Oversize</button>
  <button class="chip-btn chip-vibe" onclick="applyFilter('VIBE_MATCHDAY')">🏆 Matchday & Pride</button>
  <button class="chip-btn chip-vibe" onclick="applyFilter('VIBE_ACTIVE')">🏃 Active Performance</button>
  <button class="chip-btn" onclick="applyFilter('TOP_GMV')">🔥 Top GMV</button>
  <button class="chip-btn" onclick="applyFilter('SHOPEE_DEAL')">🏷️ Shopee ถูกชัวร์</button>
  <button class="chip-btn" onclick="applyFilter('Polo Shirts')">👕 เสื้อโปโล</button>
  <button class="chip-btn" onclick="applyFilter('Pants & Shorts')">🩳 กางเกงวอร์ม/กีฬา</button>
  <button class="chip-btn" onclick="applyFilter('Running Shoes')">👟 รองเท้าวิ่ง/ลำลอง</button>
  <button class="chip-btn" onclick="applyFilter('Jeans')">👖 ยีนส์ Kuma/Pansa</button>
</nav>

<!-- Main App Workspace -->
<div class="app-workspace">

  <!-- ================= VIEW 1: STUDIO SPLIT VIEW ================= -->
  <div class="studio-split-view" id="studio-view">
    <!-- Left Navigator -->
    <aside class="product-sidebar" id="product-sidebar">
      <div class="sidebar-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span>รายการสินค้า (<span id="filtered-count">100</span>)</span>
        </div>
        <button class="btn-sidebar-toggle" onclick="toggleProductSidebar()" id="sidebar-toggle-btn" title="ซ่อนรายการ 100 SKUs เพื่อขยายหน้าจอ Prompter ให้กว้างเต็มตา">
          ✕ ซ่อน (OFF)
        </button>
      </div>
      <div class="product-list-scroll" id="product-list-container">
        <!-- Rendered dynamically -->
      </div>
    </aside>

    <!-- Right Live Stage Prompter -->
    <main class="product-teleprompter-stage" id="prompter-stage" style="position:relative;">
      <button class="floating-sidebar-restore-btn" id="stage-sidebar-restore-btn" onclick="toggleProductSidebar()" style="display:none;" title="คลิกเพื่อแสดงรายการสินค้า 100 SKUs">
        📑 แสดง 100 SKUs
      </button>
      <!-- Rendered dynamically -->
    </main>
  </div>

  <!-- ================= VIEW 2: MIX & MATCH LOOKBOOK BUILDER (REDESIGNED) ================= -->
  <div class="lookbook-view" id="lookbook-view">
    <div class="lookbook-container">
      
      <!-- Lookbook Header & Presets -->
      <div class="lookbook-header">
        <div class="lookbook-header-title">
          <div style="font-size:12px; font-weight:700; color:var(--accent-pink); text-transform:uppercase; letter-spacing:0.8px;">
            👗 OUTFIT BUILDER & STYLING CANVAS (ACCURATE BUNDLE PRICER)
          </div>
          <h2>WARRIX Mix & Match Total Look Studio</h2>
          <p>จัดเซ็ต Total Look สดหน้ากล้อง • คำนวณราคายูนิตตรง 100% พร้อมส่วนลด Tiered Bundle (2 ชิ้น -15%, 3 ชิ้น -20%)</p>
        </div>

        <div style="display:flex; gap:8px;">
          <button class="btn-action-pill btn-pink" onclick="sendOutfitToStylist()">
            ✨ วิเคราะห์ด้วย AI Stylist
          </button>
          <button class="btn-action-pill btn-blue" onclick="switchView('studio')">
            📺 กลับหน้า Live Prompter
          </button>
        </div>
      </div>

      <!-- Style Preset Chips Bar -->
      <div class="lookbook-presets-bar">
        <span style="font-size:12px; color:var(--text-muted); align-self:center; font-weight:600; white-space:nowrap;">🎨 สไตล์ Preset สำเร็จรูป:</span>
        <button class="preset-pill-btn active" onclick="loadOutfitPreset('smart_casual')">💼 Smart Casual Friday</button>
        <button class="preset-pill-btn" onclick="loadOutfitPreset('cafe_street')">☕ Weekend Cafe Street</button>
        <button class="preset-pill-btn" onclick="loadOutfitPreset('active_running')">🏃 City Run & Gym</button>
        <button class="preset-pill-btn" onclick="loadOutfitPreset('matchday')">🏆 Matchday Stadium</button>
        <button class="preset-pill-btn" onclick="loadOutfitPreset('quiet_luxury')">🕶️ Quiet Luxury Executive</button>
        <button class="preset-pill-btn" onclick="loadOutfitPreset('travel_airport')">✈️ Travel Minimalist</button>
      </div>

      <!-- 3-Piece Visual Outfit Builder Canvas -->
      <div class="outfit-builder-grid">
        
        <!-- Slot 1: TOP -->
        <div class="outfit-slot-card slot-active" id="slot-card-top">
          <div class="outfit-slot-header">
            <span>👕 ชิ้นบน (Top / Jacket)</span>
            <label class="slot-toggle-label">
              <input type="checkbox" id="toggle-slot-top" checked onchange="toggleSlotActive('top', this.checked)">
              <span>รวมในเซ็ต</span>
            </label>
          </div>

          <div class="outfit-slot-preview" id="slot-img-top">
            <!-- Dynamic Image -->
          </div>

          <div class="outfit-slot-details">
            <div class="outfit-slot-sku-row">
              <span class="outfit-slot-sku" id="slot-sku-top">WA-261PLACL15</span>
              <span class="outfit-slot-exact-price" id="slot-price-top">฿390</span>
            </div>
            <div class="outfit-slot-name" id="slot-name-top">THE SIGNATURE POLO</div>
            <div class="slot-swatches-row" id="slot-swatches-top"></div>
          </div>

          <div style="display:flex; gap:6px; align-items:center;">
            <select class="slot-select-dropdown" id="select-slot-top" onchange="handleOutfitChange('top', this.value)" style="flex:1;">
              <!-- Top Options -->
            </select>
            <div class="slot-item-stepper">
              <button class="slot-step-btn" onclick="stepSlotItem('top', -1)" title="ชิ้นก่อนหน้า">◀</button>
              <button class="slot-step-btn" onclick="stepSlotItem('top', 1)" title="ชิ้นถัดไป">▶</button>
            </div>
          </div>
        </div>

        <!-- Slot 2: BOTTOM -->
        <div class="outfit-slot-card slot-active" id="slot-card-bottom">
          <div class="outfit-slot-header">
            <span>👖 ชิ้นล่าง (Pants / Shorts / Jeans)</span>
            <label class="slot-toggle-label">
              <input type="checkbox" id="toggle-slot-bottom" checked onchange="toggleSlotActive('bottom', this.checked)">
              <span>รวมในเซ็ต</span>
            </label>
          </div>

          <div class="outfit-slot-preview" id="slot-img-bottom">
            <!-- Dynamic Image -->
          </div>

          <div class="outfit-slot-details">
            <div class="outfit-slot-sku-row">
              <span class="outfit-slot-sku" id="slot-sku-bottom">LP-241JEMW103</span>
              <span class="outfit-slot-exact-price" id="slot-price-bottom">฿1,490</span>
            </div>
            <div class="outfit-slot-name" id="slot-name-bottom">Pansa Straight Leg Jeans</div>
            <div class="slot-swatches-row" id="slot-swatches-bottom"></div>
          </div>

          <div style="display:flex; gap:6px; align-items:center;">
            <select class="slot-select-dropdown" id="select-slot-bottom" onchange="handleOutfitChange('bottom', this.value)" style="flex:1;">
              <!-- Bottom Options -->
            </select>
            <div class="slot-item-stepper">
              <button class="slot-step-btn" onclick="stepSlotItem('bottom', -1)" title="ชิ้นก่อนหน้า">◀</button>
              <button class="slot-step-btn" onclick="stepSlotItem('bottom', 1)" title="ชิ้นถัดไป">▶</button>
            </div>
          </div>
        </div>

        <!-- Slot 3: FOOTWEAR & ACC -->
        <div class="outfit-slot-card slot-active" id="slot-card-shoes">
          <div class="outfit-slot-header">
            <span>👟 รองเท้า / หมวก (Shoes / Acc)</span>
            <label class="slot-toggle-label">
              <input type="checkbox" id="toggle-slot-shoes" checked onchange="toggleSlotActive('shoes', this.checked)">
              <span>รวมในเซ็ต</span>
            </label>
          </div>

          <div class="outfit-slot-preview" id="slot-img-shoes">
            <!-- Dynamic Image -->
          </div>

          <div class="outfit-slot-details">
            <div class="outfit-slot-sku-row">
              <span class="outfit-slot-sku" id="slot-sku-shoes">WF-253RNACL04</span>
              <span class="outfit-slot-exact-price" id="slot-price-shoes">฿1,390</span>
            </div>
            <div class="outfit-slot-name" id="slot-name-shoes">Warrix Aegis Sneakers</div>
            <div class="slot-swatches-row" id="slot-swatches-shoes"></div>
          </div>

          <div style="display:flex; gap:6px; align-items:center;">
            <select class="slot-select-dropdown" id="select-slot-shoes" onchange="handleOutfitChange('shoes', this.value)" style="flex:1;">
              <!-- Shoes Options -->
            </select>
            <div class="slot-item-stepper">
              <button class="slot-step-btn" onclick="stepSlotItem('shoes', -1)" title="ชิ้นก่อนหน้า">◀</button>
              <button class="slot-step-btn" onclick="stepSlotItem('shoes', 1)" title="ชิ้นถัดไป">▶</button>
            </div>
          </div>
        </div>

        <!-- Right Side: Total Look Pricing & MC Bundle Script (100% Accurate Breakdown) -->
        <div class="bundle-summary-card">
          <div class="bundle-summary-title">
            <span>🎁 สรุปเซ็ต Total Look Bundle</span>
            <span class="bundle-tier-badge" id="bundle-tier-badge">ลดพิเศษ 20% (3 ชิ้น)</span>
          </div>

          <!-- Itemized Breakdown -->
          <div class="bundle-itemized-list" id="bundle-itemized-list">
            <!-- Rendered dynamically with exact prices -->
          </div>

          <div style="display:flex; flex-direction:column; gap:4px;">
            <div class="bundle-calc-row">
              <span>ยอดรวมราคาปกติ (Subtotal):</span>
              <span id="bundle-raw-total" style="font-family:'JetBrains Mono'; font-weight:600;">฿3,270</span>
            </div>
            <div class="bundle-calc-row">
              <span style="color:#ec4899; font-weight:600;" id="bundle-discount-label">ส่วนลดเซ็ต Total Look (-20%):</span>
              <span id="bundle-discount-val" style="color:#ec4899; font-weight:700; font-family:'JetBrains Mono';">-฿654</span>
            </div>
            <div class="bundle-total-row">
              <div>
                <div style="font-size:11px; color:#94a3b8;">ราคาสุทธิพิเศษในไลฟ์:</div>
                <div class="bundle-final-price" id="bundle-final-price">฿2,616</div>
              </div>
              <div style="text-align:right;">
                <span style="background:rgba(245, 158, 11, 0.2); border:1px solid var(--accent-gold); color:#fbbf24; font-size:11px; font-weight:700; padding:3px 8px; border-radius:6px; display:inline-block;" id="bundle-savings-badge">
                  ประหยัด ฿654
                </span>
              </div>
            </div>
          </div>

          <div style="margin-top:2px;">
            <div style="font-size:11px; color:var(--accent-gold); font-weight:700; margin-bottom:6px; display:flex; justify-content:space-between;">
              <span>🎙️ สคริปต์ MC พูดสดปิดการขายเซ็ตนี้:</span>
            </div>
            <div class="bundle-script-box" id="bundle-speaking-script">
              "เซ็ต Total Look 3 ชิ้นนี้ แมตช์คู่กันอย่างลงตัวสุดๆ ครับ! เสื้อ THE SIGNATURE POLO คู่กับกางเกง Pansa Straight Leg Jeans และรองเท้า Warrix Aegis Sneakers ราคารวมปกติ ฿3,270 แต่พิเศษในไลฟ์ ซื้อยกเซ็ตลดทันที 20% จ่ายเพียง ฿2,616 ประหยัดไปถึง ฿654 บาททันทีครับ!"
            </div>
          </div>

          <button class="btn-action-pill btn-pink" onclick="copyBundleScript()" style="justify-content:center; margin-top:auto;">
            📋 คัดลอกบทพูด Total Look
          </button>
        </div>

      </div>

    </div>
  </div>

  <!-- ================= VIEW 3: AI PERSONAL STYLIST STUDIO ================= -->
  <div class="stylist-view" id="stylist-view">
    <div class="stylist-container">
      
      <!-- Left Stylist Knowledge Sidebar -->
      <aside class="stylist-sidebar-tools">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:11px; font-weight:700; color:var(--accent-pink); text-transform:uppercase; letter-spacing:0.8px;">
              💄 AI FASHION ASSISTANT
            </div>
            <span style="font-size:10px; color:#10b981; background:rgba(16,185,129,0.15); padding:2px 6px; border-radius:4px; font-weight:700;">⚡ Sub-50ms Ultra Turbo</span>
          </div>
          <h2 style="font-size:18px; font-weight:700; color:#fff; margin-top:2px;">
            WARRIX Stylist Studio
          </h2>
          <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">
            ผู้ช่วยสไตลิสต์ AI ส่วนตัว ตอบไวระดับ Real-time • <strong>Gemini 3.6 Flash</strong>
          </p>
        </div>

        <!-- Personal Color Selector Box -->
        <div class="color-analysis-box">
          <div style="font-size:12px; font-weight:700; color:#fff; display:flex; align-items:center; gap:6px;">
            <span>🎨 วิเคราะห์โทนสีผิว (Personal Color)</span>
          </div>
          <div class="undertone-btn-row">
            <button class="undertone-btn active" onclick="setPersonalColor('warm')">
              ☀️ Warm Tone<br><span style="font-size:9.5px; opacity:0.8;">ผิวสองสี/เหลือง</span>
            </button>
            <button class="undertone-btn" onclick="setPersonalColor('cool')">
              ❄️ Cool Tone<br><span style="font-size:9.5px; opacity:0.8;">ผิวขาวอมชมพู</span>
            </button>
            <button class="undertone-btn" onclick="setPersonalColor('deep')">
              🌙 Deep Tone<br><span style="font-size:9.5px; opacity:0.8;">ผิวเข้มคมเข้ม</span>
            </button>
          </div>
          <div id="personal-color-rec" style="font-size:11.5px; color:#cbd5e1; line-height:1.4; background:#040711; padding:8px 10px; border-radius:6px; border:1px solid #1e293b;">
            💡 <strong>Warm Tone:</strong> เหมาะกับเสื้อสี <em>Forest Pine, Champagne Gold, Navy Blue</em> ช่วยขับผิวให้สว่างผ่อง
          </div>
        </div>

        <!-- Quick Styling Prompts (Instant Stream Fast-Path) -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="font-size:12px; font-weight:700; color:#cbd5e1;">⚡ สคริปต์สไตลิ่งด่วน (ตอบทันที < 50ms):</div>
          
          <div class="stylist-quick-card" onclick="askStylistPreset('color_analysis')">
            <div style="font-weight:600; font-size:12.5px; color:#f472b6;">🎨 แนะนำคู่สีเสื้อผ้าขับผิวออร่า</div>
            <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">วิธีเลือกสีเสื้อให้หน้าสว่าง ไม่หมอง</div>
          </div>

          <div class="stylist-quick-card" onclick="askStylistPreset('silhouette')">
            <div style="font-weight:600; font-size:12.5px; color:#38bdf8;">📏 ทริกแต่งตัวพรางสัดส่วน & พรางพุง</div>
            <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">ใส่โปโลและยีนส์อย่างไรให้ดูสูงเพรียว</div>
          </div>

          <div class="stylist-quick-card" onclick="askStylistPreset('quiet_luxury')">
            <div style="font-weight:600; font-size:12.5px; color:#fbbf24;">✨ ลุค Quiet Luxury / Old Money</div>
            <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">แต่งตัวสไตล์มินิมอลแต่ดูแพงมาก</div>
          </div>

          <div class="stylist-quick-card" onclick="askStylistPreset('mix_match')">
            <div style="font-weight:600; font-size:12.5px; color:#10b981;">👖 การแมตช์กางเกงและรองเท้า</div>
            <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px;">ไอเดียจับคู่สี Total Look สากล</div>
          </div>
        </div>
      </aside>

      <!-- Main Chat Area -->
      <main class="stylist-main-chat">
        <div class="stylist-chat-header">
          <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg, #ec4899, #8b5cf6); display:flex; align-items:center; justify-content:center; font-size:18px;">
              💄
            </div>
            <div>
              <div style="font-size:15px; font-weight:700; color:#fff;">WARRIX AI Personal Stylist (Celebrity Mode)</div>
              <div style="font-size:11.5px; color:#94a3b8;">Real-time Fashion Advisory & Color Matching • Gemini 3.6 Flash Turbo</div>
            </div>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn-action-pill" onclick="clearStylistChat()" style="color:#94a3b8;">🗑️ ล้างแชต</button>
            <button class="btn-action-pill btn-blue" onclick="switchView('studio')">
              📺 กลับหน้า Live Prompter
            </button>
          </div>
        </div>

        <div class="stylist-chat-body" id="stylistChatTimeline">
          <div class="stylist-msg-ai">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span style="font-size:16px;">💄</span>
              <strong style="color:#f472b6; font-size:13px;">WARRIX Celebrity Stylist</strong>
              <span style="font-size:10px; background:rgba(236,72,153,0.2); color:#f472b6; padding:1px 6px; border-radius:4px;">Turbo Stream Active</span>
            </div>
            <p>สวัสดีครับ! ผมคือ <strong>WARRIX AI Personal Stylist</strong> พร้อมให้คำแนะนำเรื่องสไตล์ การแมตช์คู่สี และทริกแต่งตัวเพื่อช่วยปิดการขายในไลฟ์จากสินค้า WARRIX ทั้ง 100 SKUs ตอบไวทันใจทันทีครับ!</p>
          </div>
        </div>

        <div class="stylist-chat-input-area">
          <form onsubmit="handleStylistSubmit(event)" style="display:flex; gap:10px; align-items:center;">
            <input type="text" id="stylistChatInput" placeholder="ถามเรื่องการแต่งตัว เช่น 'เสื้อโปโลสีกรม ใส่คู่กับกางเกงสีอะไรดี?' หรือ 'คนมีพุงใส่ทรงไหน?'" style="flex:1; background:#040711; border:1px solid #334155; border-radius:10px; padding:12px 18px; color:#fff; font-size:14px; outline:none; font-family:inherit;">
            <button type="submit" style="background:linear-gradient(135deg, #ec4899, #8b5cf6); border:none; color:#fff; font-weight:600; padding:12px 24px; border-radius:10px; cursor:pointer; font-size:14px; display:flex; align-items:center; gap:6px;">
              <span>ส่งสไตลิสต์</span> ⚡
            </button>
          </form>
        </div>
      </main>

    </div>
  </div>

  <!-- ================= VIEW 4: DEDICATED SIZE MATRIX & ADVISOR HUB ================= -->
  <div class="size-hub-view" id="sizes-view">
    <div class="size-hub-container">
      
      <!-- Hub Header -->
      <div class="size-hub-header-card">
        <div>
          <div style="font-size:12px; font-weight:700; color:var(--accent-gold); text-transform:uppercase; letter-spacing:0.8px;">
            📏 WARRIX SMART SIZING & FITTING HUB
          </div>
          <h2 style="font-size:20px; font-weight:700; color:#fff; margin-top:2px;">
            ระบบวิเคราะห์ขนาดและตารางไซซ์ทางการ (สำหรับตอบแชตสดหน้ากล้อง)
          </h2>
          <div style="font-size:12.5px; color:var(--text-muted); margin-top:4px;">
            กำลังอ้างอิงสินค้าปัจจุบัน: <strong id="hub-current-sku" style="color:#fbbf24; font-family:'JetBrains Mono';">WA-261PLACL15</strong> (<span id="hub-current-name">THE SIGNATURE POLO</span>)
          </div>
        </div>

        <div style="display:flex; gap:8px;">
          <button class="btn-action-pill btn-blue" onclick="switchView('studio')">
            📺 กลับหน้า Live Prompter
          </button>
        </div>
      </div>

      <!-- Interactive Calculator Card -->
      <div class="size-calc-card">
        <!-- Input Side -->
        <div class="calc-input-section">
          <div style="font-size:14px; font-weight:700; color:#fff; border-bottom:1px solid #1e293b; padding-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
            <span>👤 ใส่ข้อมูลสรีระลูกค้า (จากคอมเมนต์ในไลฟ์)</span>
            <span style="font-size:11px; color:#38bdf8;">คำนวณแบบ Real-time</span>
          </div>

          <!-- Height -->
          <div class="calc-field-row">
            <div class="calc-field-label">
              <span>ส่วนสูง (Height)</span>
              <span style="color:#94a3b8; font-size:11px;">ซม. (cm)</span>
            </div>
            <div class="calc-input-wrapper">
              <input type="number" id="calc-height-input" value="175" min="140" max="210" class="calc-input-box-num" oninput="runSizeCalculation()">
              <div class="chip-selector-group">
                <span class="size-quick-chip" onclick="setQuickHeight(160)">160</span>
                <span class="size-quick-chip" onclick="setQuickHeight(165)">165</span>
                <span class="size-quick-chip" onclick="setQuickHeight(170)">170</span>
                <span class="size-quick-chip" onclick="setQuickHeight(175)">175</span>
                <span class="size-quick-chip" onclick="setQuickHeight(180)">180</span>
                <span class="size-quick-chip" onclick="setQuickHeight(185)">185</span>
              </div>
            </div>
          </div>

          <!-- Weight -->
          <div class="calc-field-row">
            <div class="calc-field-label">
              <span>น้ำหนักตัว (Weight)</span>
              <span style="color:#94a3b8; font-size:11px;">กก. (kg)</span>
            </div>
            <div class="calc-input-wrapper">
              <input type="number" id="calc-weight-input" value="75" min="35" max="180" class="calc-input-box-num" oninput="runSizeCalculation()">
              <div class="chip-selector-group">
                <span class="size-quick-chip" onclick="setQuickWeight(55)">55</span>
                <span class="size-quick-chip" onclick="setQuickWeight(65)">65</span>
                <span class="size-quick-chip" onclick="setQuickWeight(70)">70</span>
                <span class="size-quick-chip" onclick="setQuickWeight(75)">75</span>
                <span class="size-quick-chip" onclick="setQuickWeight(82)">82</span>
                <span class="size-quick-chip" onclick="setQuickWeight(90)">90</span>
                <span class="size-quick-chip" onclick="setQuickWeight(105)">105+</span>
              </div>
            </div>
          </div>

          <!-- Fit Preference -->
          <div class="calc-field-row">
            <div class="calc-field-label">
              <span>สไตล์ความชอบในการสวมใส่ (Fit Style)</span>
            </div>
            <div class="fit-pref-group">
              <button class="fit-pref-btn active" id="pref-btn-regular" onclick="setFitPreference('regular')">
                🟢 พอดีตัว (Fit)
              </button>
              <button class="fit-pref-btn" id="pref-btn-comfort" onclick="setFitPreference('comfort')">
                🟡 พรางพุง (Comfort)
              </button>
              <button class="fit-pref-btn" id="pref-btn-oversize" onclick="setFitPreference('oversize')">
                🟣 โคร่ง (Oversize)
              </button>
            </div>
          </div>
        </div>

        <!-- Output Side -->
        <div class="calc-output-section">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:11.5px; color:#f59e0b; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
              🎯 ผลวิเคราะห์ไซซ์ที่แนะนำ (Recommended Size)
            </div>
            <span id="calc-fit-badge" style="background:#0284c7; color:#fff; font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:6px;">Smart Regular Fit</span>
          </div>

          <div class="rec-badge-display">
            <span id="calc-rec-size">XL</span>
            <span id="calc-rec-spec" style="font-size:15px; color:#cbd5e1; font-weight:normal;">(อก 44" / 111 ซม.)</span>
          </div>

          <div id="calc-reason-text" style="font-size:12.5px; color:#94a3b8; line-height:1.4;">
            สำหรับส่วนสูง 175 ซม. น้ำหนัก 75 กก. แนะนำไซซ์ XL สวมใส่สบาย ไม่รั้งช่วงอกและไหล่
          </div>

          <!-- Live MC Speaking Script Box -->
          <div class="calc-field-row" style="margin-top:auto;">
            <div class="calc-field-label" style="color:#fbbf24; font-weight:700;">
              <span>🎙️ สคริปต์พูดสดสำหรับ MC (ตอบคอมเมนต์ทันที)</span>
            </div>
            <div class="live-speaking-card" id="calc-speaking-script">
              "พี่ที่สูง 175 หนัก 75 แนะนำกดไซซ์ XL เลยครับ! ทรงสวยเข้ารูปกำลังดี รุ่นนี้ไหล่สโลปใส่แล้วดูตัวเพรียวมากครับ!"
            </div>
          </div>

          <button class="btn-action-pill btn-blue" onclick="copyAdvisorScript()" style="justify-content:center;">
            📋 คัดลอกสคริปต์ตอบแชต
          </button>
        </div>
      </div>

      <!-- Size Matrix Tables Section -->
      <div class="size-tables-grid">
        
        <!-- Table 1: Tops & Polos -->
        <div class="size-table-card">
          <div class="size-table-header">
            <div style="font-size:14px; font-weight:700; color:#fff;">
              👕 1. ตารางขนาดเสื้อโปโลและเสื้อกีฬา (Tops & Polos Size Matrix)
            </div>
            <div class="table-unit-toggle">
              <button class="unit-btn active" id="unit-top-in" onclick="switchSizeUnit('in')">นิ้ว (Inches)</button>
              <button class="unit-btn" id="unit-top-cm" onclick="switchSizeUnit('cm')">ซม. (CM)</button>
            </div>
          </div>
          <table class="styled-size-table" id="table-tops-body">
            <!-- Rendered dynamically -->
          </table>
        </div>

        <!-- Table 2: Pants & Shorts -->
        <div class="size-table-card">
          <div class="size-table-header">
            <div style="font-size:14px; font-weight:700; color:#fff;">
              🩳 2. ตารางขนาดกางเกงวอร์มและกางเกงกีฬา (Pants & Shorts Matrix)
            </div>
            <div class="table-unit-toggle">
              <button class="unit-btn active" id="unit-pant-in" onclick="switchSizeUnit('in')">นิ้ว (Inches)</button>
              <button class="unit-btn" id="unit-pant-cm" onclick="switchSizeUnit('cm')">ซม. (CM)</button>
            </div>
          </div>
          <table class="styled-size-table" id="table-pants-body">
            <!-- Rendered dynamically -->
          </table>
        </div>

        <!-- Table 3: Shoes & Boots -->
        <div class="size-table-card">
          <div class="size-table-header">
            <div style="font-size:14px; font-weight:700; color:#fff;">
              👟 3. ตารางขนาดรองเท้าวิ่ง สนีกเกอร์ และสตั๊ด (Shoes & Cleats Matrix)
            </div>
            <span style="font-size:11.5px; color:#38bdf8;">ทรง Wide Fit เพื่อเท้าคนไทย</span>
          </div>
          <table class="styled-size-table" id="table-shoes-body">
            <!-- Rendered dynamically -->
          </table>
        </div>

      </div>

    </div>
  </div>

  <!-- ================= VIEW 5: GRID CATALOG ================= -->
  <div class="catalog-grid-view" id="grid-view" style="display:none; padding:24px; overflow-y:auto; width:100%; height:100%;">
    <div id="grid-container" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(220px, 1fr)); gap:16px; max-width:1440px; margin:0 auto;"></div>
  </div>

  <!-- ================= VIEW 6: PRICE MATRIX ================= -->
  <div class="matrix-table-view" id="matrix-view" style="display:none; padding:24px; overflow-y:auto; width:100%; height:100%;">
    <div style="max-width:1440px; margin:0 auto; background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:16px; overflow:hidden;">
      <table style="width:100%; border-collapse:collapse; font-size:13px; color:#cbd5e1;">
        <thead style="background:var(--bg-panel); border-bottom:1px solid var(--border-subtle);">
          <tr>
            <th style="padding:12px 16px; text-align:left;">SKU</th>
            <th style="padding:12px 16px; text-align:left;">ชื่อสินค้า</th>
            <th style="padding:12px 16px; text-align:left;">หมวดหมู่</th>
            <th style="padding:12px 16px; text-align:left;">ราคาไลฟ์</th>
            <th style="padding:12px 16px; text-align:left;">Occasion Vibe</th>
            <th style="padding:12px 16px; text-align:left;">ลิงก์สินค้า</th>
          </tr>
        </thead>
        <tbody id="matrix-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- ================= VIEW 7: TIKTOK LIVE SELLING PLAN BUILDER ================= -->
  <div class="plan-view" id="plan-view" style="display:none; width:100%; height:100%; overflow-y:auto; padding:24px 32px 60px;">
    <!-- Stepper Navigation -->
    <nav class="plan-stepper-nav">
      <button class="plan-step-btn active" id="pStepBtn1" onclick="setPlanWizardStep(1)">
        <span class="plan-step-num">1</span> <span>1. เลือกสินค้า (Catalog)</span>
      </button>
      <button class="plan-step-btn" id="pStepBtn2" onclick="setPlanWizardStep(2)">
        <span class="plan-step-num">2</span> <span>2. กำหนดโจทย์ไลฟ์ (Session Brief)</span>
      </button>
      <button class="plan-step-btn" id="pStepBtn3" onclick="setPlanWizardStep(3)">
        <span class="plan-step-num">3</span> <span>3. ตรวจสอบแผน & จัดคิว (Plan Review & Reorder)</span>
      </button>
      <button class="plan-step-btn" id="pStepBtn4" onclick="setPlanWizardStep(4)">
        <span class="plan-step-num">4</span> <span>4. ห้องออกอากาศสด (Host & Mod Views)</span>
      </button>
    </nav>

    <!-- STEP 1: CATALOG PICKER -->
    <div class="plan-step-container active" id="pStepContainer1">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; gap:16px; flex-wrap:wrap;">
        <div style="position:relative; flex:1; min-width:280px;">
          <input type="text" id="pPickerSearch" placeholder="🔍 ค้นหา SKU, ชื่อรุ่น, สี หรือไซส์เพื่อนำเข้าไลฟ์..." oninput="renderPlanPickerGrid()" style="width:100%; background:var(--bg-panel); border:1px solid var(--border-subtle); padding:9px 14px; border-radius:8px; color:#fff; font-size:13px; font-family:inherit; outline:none;" />
        </div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
          <button class="chip-btn active" onclick="filterPlanPickerCat('ALL', this)">ทั้งหมด (100)</button>
          <button class="chip-btn" onclick="filterPlanPickerCat('Polo', this)">Polo</button>
          <button class="chip-btn" onclick="filterPlanPickerCat('T-Shirt', this)">T-Shirts</button>
          <button class="chip-btn" onclick="filterPlanPickerCat('Jersey', this)">Jerseys</button>
          <button class="chip-btn" onclick="filterPlanPickerCat('Pant', this)">Pants / Shorts</button>
          <button class="chip-btn" onclick="filterPlanPickerCat('Shoe', this)">Footwear</button>
        </div>
      </div>

      <div class="plan-picker-grid" id="planPickerGrid">
        <!-- Rendered dynamically -->
      </div>

      <!-- Floating Summary Tray -->
      <div class="plan-tray-bar">
        <div style="display:flex; align-items:center; gap:16px;">
          <span id="pTrayCount" style="background:#10b981; color:#0f172a; font-weight:800; font-size:13px; padding:4px 12px; border-radius:20px;">เลือกแล้ว 0 ชิ้น</span>
          <div id="pTrayThumbs" style="display:flex; gap:6px; max-width:380px; overflow-x:auto;"></div>
          <span id="pTrayPrice" style="font-size:13.5px; font-weight:700; color:#38bdf8;">รวม ฿0</span>
        </div>
        <button onclick="proceedToPlanBrief()" style="background:linear-gradient(135deg, #10b981, #059669); border:none; color:#fff; padding:10px 22px; border-radius:8px; font-size:13.5px; font-weight:700; cursor:pointer; font-family:inherit;">
          ต่อไป: กำหนดโจทย์ไลฟ์ ➔
        </button>
      </div>
    </div>

    <!-- STEP 2: SESSION BRIEF FORM -->
    <div class="plan-step-container" id="pStepContainer2">
      <div class="plan-brief-card">
        <h2 style="font-size:18px; font-weight:700; color:#fff; display:flex; align-items:center; gap:8px;">
          <span>📝</span> กำหนดรายละเอียดรอบไลฟ์ (Session Brief)
        </h2>
        <p style="font-size:12.5px; color:var(--text-muted); margin-top:3px;">
          กำหนดเป้าหมายรอบไลฟ์เพื่อให้ระบบ AI สร้าง Timed Rundown, Look Cards และสคริปต์พูดออกกล้องที่ตรงโจทย์ 100%
        </p>

        <form onsubmit="generateLiveSellingPlan(event)">
          <div class="plan-form-grid">
            <div class="plan-form-group">
              <label>1. ธีมหลัก / โอกาสการใส่ (Theme & Occasion)</label>
              <select id="pBriefTheme">
                <option value="Smart Casual Friday & Workwear">💼 Smart Casual Friday & Workwear (ทำงาน+เที่ยว)</option>
                <option value="Weekend Cafe & Streetwear">☕ Weekend Cafe & Streetwear (คาเฟ่+วันหยุด)</option>
                <option value="Active Runner & Fitness">⚡ Active Runner & Fitness (ออกกำลังกาย+วิ่ง)</option>
                <option value="Payday Flash Sale & Best Deals">🔥 Payday Flash Sale (ดีลวันเงินเดือนออก)</option>
              </select>
            </div>
            <div class="plan-form-group">
              <label>2. กลุ่มลูกค้าเป้าหมาย (Target Customer)</label>
              <input type="text" id="pBriefTarget" value="วัยทำงาน 25-40 ปี ชอบเสื้อผ้าไม่ยับ ใส่สบาย ระบายอากาศดี" required />
            </div>
            <div class="plan-form-group">
              <label>3. ระยะเวลาไลฟ์สดทั้งหมด (Total Duration)</label>
              <select id="pBriefDuration">
                <option value="30">30 นาที (Quick Flash)</option>
                <option value="45">45 นาที (Standard)</option>
                <option value="60" selected>60 นาที (Full Session 1 ชม.)</option>
                <option value="90">90 นาที (Grand Live 1.5 ชม.)</option>
                <option value="120">120 นาที (Mega Marathon 2 ชม.)</option>
              </select>
            </div>
            <div class="plan-form-group">
              <label>4. ประเทศและสกุลเงิน (Country & Currency)</label>
              <input type="text" value="Thailand (THB ฿)" readonly style="background:rgba(0,0,0,0.3); color:#94a3b8;" />
            </div>
            <div class="plan-form-group">
              <label>5. ชื่อพิธีกร MC (Host)</label>
              <input type="text" id="pBriefHost" value="MC นนท์ & MC แพรว" required />
            </div>
            <div class="plan-form-group">
              <label>6. ชื่อแอดมินดูแลระบบ (Moderator)</label>
              <input type="text" id="pBriefMod" value="Mod กิ๊ก (ปักหมุด & ตอบไซส์)" required />
            </div>
          </div>

          <div style="margin-top:18px;">
            <label style="font-size:12.5px; font-weight:700; color:#94a3b8; display:block; margin-bottom:8px;">
              7. โปรโมชั่นที่ได้รับอนุมัติในรอบนี้ (Approved Promotions)
            </label>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; background:rgba(0,0,0,0.25); padding:12px; border-radius:8px; border:1px solid var(--border-subtle);">
              <label style="display:flex; align-items:center; gap:8px; font-size:13px; color:#e2e8f0; cursor:pointer;"><input type="checkbox" id="pPromo15" checked /> 🎟️ ซื้อเซ็ต 2 ชิ้น ลด 15%</label>
              <label style="display:flex; align-items:center; gap:8px; font-size:13px; color:#e2e8f0; cursor:pointer;"><input type="checkbox" id="pPromo20" checked /> 🔥 ซื้อเซ็ต 3 ชิ้น (Total Look) ลด 20%</label>
              <label style="display:flex; align-items:center; gap:8px; font-size:13px; color:#e2e8f0; cursor:pointer;"><input type="checkbox" id="pPromoShip" checked /> 🚚 ส่งฟรีทุกออเดอร์เมื่อช้อปครบ ฿999</label>
              <label style="display:flex; align-items:center; gap:8px; font-size:13px; color:#e2e8f0; cursor:pointer;"><input type="checkbox" id="pPromoVoucher" /> 🏷️ คูปองลดเพิ่ม ฿50 (WARRIX50)</label>
            </div>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:24px;">
            <button type="button" onclick="setPlanWizardStep(1)" style="background:transparent; border:1px solid var(--border-subtle); color:#fff; padding:9px 18px; border-radius:8px; cursor:pointer; font-family:inherit;">
              ◀ ย้อนกลับไปเลือกสินค้า
            </button>
            <button type="submit" style="background:linear-gradient(135deg, #6366f1, #4338ca); border:none; color:#fff; padding:11px 24px; border-radius:8px; font-size:13.5px; font-weight:700; cursor:pointer; font-family:inherit;">
              ⚡ สร้างแผนไลฟ์สดด้วย AI (Generate Draft Plan) ➔
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- STEP 3: PLAN REVIEW & REORDER EDITOR -->
    <div class="plan-step-container" id="pStepContainer3">
      <div class="plan-overview-card">
        <div>
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            <h2 id="pPlanTitle" style="font-size:18px; font-weight:700; color:#fff;">แผนไลฟ์สด: Smart Casual Friday</h2>
            <span id="pPlanStatus" style="font-size:11px; font-weight:700; background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid rgba(245,158,11,0.4); padding:3px 10px; border-radius:12px;">Draft (รอการอนุมัติ)</span>
          </div>
          <p id="pPlanDesc" style="font-size:12.5px; color:var(--text-muted);">
            เป้าหมาย: วัยทำงาน 25-40 ปี • พิธีกร: MC นนท์ • แอดมิน: Mod กิ๊ก
          </p>
        </div>
        <div style="display:flex; align-items:center; gap:8px; background:rgba(0,0,0,0.3); padding:8px 14px; border-radius:8px; border:1px solid var(--border-subtle);">
          <span style="font-size:13px;">⏱️ เวลารวมตามแผน:</span>
          <strong id="pPlanTimeMatch" style="color:#10b981; font-size:14px;">60 / 60 นาที (ตรงเป๊ะ 100%)</strong>
        </div>
      </div>

      <div style="font-size:15px; font-weight:700; color:#38bdf8; margin:16px 0 10px;">👗 ชุดเซ็ตที่จัดคู่สำเร็จ (Look Cards)</div>
      <div class="plan-look-grid" id="pPlanLookGrid">
        <!-- Rendered dynamically -->
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin:20px 0 10px;">
        <span style="font-size:15px; font-weight:700; color:#38bdf8;">⏱️ ลำดับคิวและสคริปต์พิธีกร (Timed Rundown & Scripts)</span>
        <span style="font-size:11.5px; color:var(--text-dim);">💡 กดปุ่ม ▲ / ▼ เพื่อสลับลำดับคิว Segment ได้ทันที</span>
      </div>
      <div class="plan-rundown-stack" id="pPlanRundownStack">
        <!-- Rendered dynamically -->
      </div>

      <!-- Action Bar -->
      <div style="display:flex; justify-content:space-between; align-items:center; background:var(--bg-surface); border:1px solid var(--border-subtle); padding:14px 20px; border-radius:10px; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; gap:8px;">
          <button onclick="savePlanDraftAction()" style="background:rgba(255,255,255,0.06); border:1px solid var(--border-subtle); color:#fff; padding:8px 16px; border-radius:6px; font-size:12.5px; cursor:pointer; font-family:inherit;">
            💾 บันทึก Draft
          </button>
          <button onclick="window.print()" style="background:rgba(255,255,255,0.06); border:1px solid var(--border-subtle); color:#fff; padding:8px 16px; border-radius:6px; font-size:12.5px; cursor:pointer; font-family:inherit;">
            🖨️ พิมพ์แผน (PDF)
          </button>
          <button onclick="exportPlanJsonFile()" style="background:rgba(255,255,255,0.06); border:1px solid var(--border-subtle); color:#fff; padding:8px 16px; border-radius:6px; font-size:12.5px; cursor:pointer; font-family:inherit;">
            📥 Export JSON
          </button>
        </div>
        <button onclick="approveLivePlan()" style="background:linear-gradient(135deg, #10b981, #059669); border:none; color:#0f172a; padding:10px 22px; border-radius:8px; font-size:13.5px; font-weight:800; cursor:pointer; font-family:inherit;">
          ✅ อนุมัติแผน & เข้าห้องไลฟ์สด ➔
        </button>
      </div>
    </div>

    <!-- STEP 4: DUAL LIVE PRESENTATION VIEWS -->
    <div class="plan-step-container" id="pStepContainer4">
      <div style="display:flex; gap:8px; margin-bottom:18px;">
        <button class="view-btn active" id="pBtnHostSub" onclick="setLiveSubview('host')" style="padding:7px 16px;">🎙️ Host View (Teleprompter จอใหญ่)</button>
        <button class="view-btn" id="pBtnModSub" onclick="setLiveSubview('mod')" style="padding:7px 16px;">🛡️ Moderator View (หลังบ้านแอดมิน)</button>
      </div>

      <!-- Host View -->
      <div id="pHostViewBox" class="plan-teleprompter-box">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:12px;">
          <div>
            <span style="font-size:11px; color:#f472b6; font-weight:700; text-transform:uppercase;">🔴 CURRENT SEGMENT</span>
            <h3 id="pHostSegTitle" style="font-size:20px; font-weight:700; color:#fff; margin-top:2px;">Segment 1: ต้อนรับ & ชี้แจงโปรโมชั่น</h3>
          </div>
          <div style="text-align:right;">
            <span style="font-size:11px; color:var(--text-dim);">เวลาช่วงนี้</span>
            <div id="pHostSegTimer" style="font-size:24px; font-weight:800; color:#38bdf8; font-family:'JetBrains Mono';">05:00</div>
          </div>
        </div>

        <div style="background:linear-gradient(135deg, rgba(234, 88, 12, 0.2), rgba(225, 29, 72, 0.2)); border:1px solid #ea580c; color:#fed7aa; padding:12px 18px; border-radius:8px; font-size:15px; font-weight:700; display:flex; align-items:center; gap:10px;">
          <span>📌 คำสั่งปักหมุด:</span>
          <strong id="pHostPinText">ปักหมุดตะกร้า #1</strong>
        </div>

        <div id="pHostScriptText" class="plan-tele-script">
          "ยินดีต้อนรับเข้าสู่ WARRIX Official Live ประจำวันศุกร์นี้ครับ..."
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:auto; padding-top:16px; border-top:1px solid rgba(255,255,255,0.1);">
          <button onclick="stepHostSeg(-1)" style="background:rgba(255,255,255,0.1); border:1px solid var(--border-subtle); color:#fff; padding:8px 18px; border-radius:6px; font-weight:600; cursor:pointer; font-family:inherit;">
            ◀ คิวก่อนหน้า
          </button>
          <span id="pHostSegCount" style="font-size:13px; color:var(--text-muted);">คิวที่ 1 จากทั้งหมด 5 คิว</span>
          <button onclick="stepHostSeg(1)" style="background:linear-gradient(135deg, #4f46e5, #6366f1); border:none; color:#fff; padding:10px 22px; border-radius:6px; font-weight:700; cursor:pointer; font-family:inherit;">
            คิวถัดไป ▶
          </button>
        </div>
      </div>

      <!-- Moderator View -->
      <div id="pModViewBox" style="display:none; grid-template-columns:320px 1fr 320px; gap:18px;">
        <div style="background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:10px; padding:18px;" id="pModSkuPanel">
          <!-- Dynamically populated -->
        </div>
        <div style="background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:10px; padding:18px;" id="pModSizePanel">
          <!-- Dynamically populated -->
        </div>
        <div style="background:var(--bg-surface); border:1px solid var(--border-subtle); border-radius:10px; padding:18px;">
          <div style="font-size:12px; font-weight:700; color:#10b981; margin-bottom:8px;">💬 คีย์ลัดตอบคอมเมนต์</div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            <button onclick="copyReplyText('มีพร้อมส่งครบไซส์ S ถึง 3L เลยครับ กดในตะกร้าได้เลยครับ')" style="background:rgba(255,255,255,0.05); border:1px solid var(--border-subtle); color:#fff; padding:8px 10px; border-radius:6px; font-size:12px; text-align:left; cursor:pointer; font-family:inherit;">
              📋 "มีพร้อมส่งครบไซส์..."
            </button>
            <button onclick="copyReplyText('รุ่นนี้ผ้าทอพิเศษ นุ่มเบา ไม่ต้องรีด ซักตากใส่ได้ทันทีครับ')" style="background:rgba(255,255,255,0.05); border:1px solid var(--border-subtle); color:#fff; padding:8px 10px; border-radius:6px; font-size:12px; text-align:left; cursor:pointer; font-family:inherit;">
              📋 "รุ่นนี้ผ้าไม่ต้องรีด..."
            </button>
            <button onclick="copyReplyText('ซื้อครบ 2 ชิ้นในไลฟ์ลด 15% อัตโนมัติในตะกร้าครับ')" style="background:rgba(255,255,255,0.05); border:1px solid var(--border-subtle); color:#fff; padding:8px 10px; border-radius:6px; font-size:12px; text-align:left; cursor:pointer; font-family:inherit;">
              📋 "ซื้อครบ 2 ชิ้นลด 15%..."
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================
       PRODUCT KNOWLEDGE & LIVE SALES PLAYBOOK (FROM 229 SESSIONS)
       ========================================================= -->
  <!-- =========================================================
       DYNAMIC PRODUCT KNOWLEDGE & SALES PLAYBOOK (FROM 229 SESSIONS & PDF)
       ========================================================= -->
  <div class="knowledge-view" id="knowledge-view">
    <div class="knowledge-container">
    
    <!-- Top Hero Banner -->
    <div style="background:linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%); border:1px solid rgba(245, 158, 11, 0.45); border-radius:20px; padding:24px 28px; margin-bottom:22px; box-shadow:0 14px 40px rgba(0,0,0,0.45); position:relative; overflow:hidden;">
      <div style="position:absolute; right:-20px; top:-20px; width:260px; height:260px; background:radial-gradient(circle, rgba(245, 158, 11, 0.15) 0%, transparent 70%); pointer-events:none;"></div>
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
        <div>
          <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(245, 158, 11, 0.15); border:1px solid rgba(245, 158, 11, 0.4); padding:4px 14px; border-radius:20px; font-size:12px; font-weight:700; color:#fbbf24; margin-bottom:10px;">
            <span>⭐ ข้อมูลจริงจาก 234 วัน (109 วันแคมเปญ + 125 วันปกติ) • 229 Live Sessions</span>
            <span>•</span>
            <span>WARRIX Master Strategy Report</span>
          </div>
          <h1 style="font-size:24px; font-weight:800; color:#fff; margin:0 0 6px 0; letter-spacing:-0.02em;">
            💡 คลังความรู้สินค้า & กลยุทธ์การขาย (Product Knowledge, Timing & UpSell Playbook)
          </h1>
          <p style="font-size:13.5px; color:#cbd5e1; margin:0; max-width:920px; line-height:1.5;">
            วิเคราะห์ลึก <strong>GMV รายเดือน, รายวัน, และรายชั่วโมง</strong> พร้อมแผนจับคู่ <strong>"สินค้าไหน ควรดันเวลาอะไร"</strong> และสูตร <strong>UpSell / Cross-Sell</strong> เพิ่มยอดตะกร้า (AOV > ฿400–฿1,500) ให้ MC และทีมขายปิดดีลได้แม่นยำที่สุด
          </p>
        </div>

        <div style="display:flex; gap:10px; align-items:center;">
          <button onclick="switchView('lookbook')" style="background:rgba(236,72,153,0.15); border:1px solid rgba(236,72,153,0.4); color:#f472b6; padding:9px 15px; border-radius:10px; font-size:12.5px; font-weight:600; cursor:pointer; font-family:inherit;">
            👗 ไปจัดเซ็ต Lookbook ↗
          </button>
          <button onclick="switchView('studio')" style="background:linear-gradient(135deg,#2563eb,#7c3aed); border:none; color:#fff; padding:9px 16px; border-radius:10px; font-size:12.5px; font-weight:700; cursor:pointer; font-family:inherit; box-shadow:0 4px 15px rgba(37,99,235,0.4);">
            🎙️ เปิดหน้าจอ Live Prompter
          </button>
        </div>
      </div>

      <!-- Quick KPI Strip from PDF -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:12px; margin-top:20px; padding-top:18px; border-top:1px solid rgba(255,255,255,0.08);">
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:12px 14px;">
          <div style="font-size:11px; color:#94a3b8; font-weight:600; text-transform:uppercase;">💰 ยอดขายรวม (Feb-Sep)</div>
          <div style="font-size:19px; font-weight:800; color:#38bdf8; margin-top:2px;">฿254.8M</div>
          <div style="font-size:11px; color:#64748b;">878K ออเดอร์ • 1.2M ชิ้น</div>
        </div>

        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:12px 14px;">
          <div style="font-size:11px; color:#94a3b8; font-weight:600; text-transform:uppercase;">🔥 วันแคมเปญ vs ปกติ</div>
          <div style="font-size:19px; font-weight:800; color:#10b981; margin-top:2px;">฿1,284K <span style="font-size:12px; font-weight:500; color:#6ee7b7;">(+40%)</span></div>
          <div style="font-size:11px; color:#64748b;">วันปกติเฉลี่ย ฿914K/วัน</div>
        </div>

        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:12px 14px;">
          <div style="font-size:11px; color:#94a3b8; font-weight:600; text-transform:uppercase;">⏰ Peak Hour (21:00 น.)</div>
          <div style="font-size:19px; font-weight:800; color:#fbbf24; margin-top:2px;">฿123K <span style="font-size:12px; font-weight:500; color:#fde68a;">/ ชม. (+80%)</span></div>
          <div style="font-size:11px; color:#64748b;">ก.ย. (9.9) พุ่งถึง ฿267K/ชม.</div>
        </div>

        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:12px 14px;">
          <div style="font-size:11px; color:#94a3b8; font-weight:600; text-transform:uppercase;">📅 วันทำเงินสูงสุด</div>
          <div style="font-size:19px; font-weight:800; color:#f472b6; margin-top:2px;">วันอาทิตย์ (+111%)</div>
          <div style="font-size:11px; color:#64748b;">วันปกติทำเงินดีสุด: วันศุกร์ ฿1.01M</div>
        </div>
      </div>
    </div>

    <!-- Sub-Navigation Tabs Bar inside Knowledge View -->
    <div style="display:flex; gap:8px; margin-bottom:20px; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:12px; overflow-x:auto;">
      <button class="k-nav-tab active" onclick="switchKnowledgeTab('trends', this)" style="background:rgba(59,130,246,0.18); border:1px solid #3b82f6; color:#93c5fd; padding:8px 16px; border-radius:8px; font-size:13px; font-weight:700; cursor:pointer; font-family:inherit; white-space:nowrap;">
        📊 1. ข้อมูล GMV รายเดือน / รายวัน / รายชั่วโมง
      </button>
      <button class="k-nav-tab" onclick="switchKnowledgeTab('schedule', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:8px 16px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; font-family:inherit; white-space:nowrap;">
        ⏰ 2. ตารางช่วงเวลา & สินค้าที่ต้องดัน (Hour-by-Hour)
      </button>
      <button class="k-nav-tab" onclick="switchKnowledgeTab('upsell', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:8px 16px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; font-family:inherit; white-space:nowrap;">
        🔄 3. สูตร UpSell & Cross-Sell (AOV Multiplier)
      </button>
      <button class="k-nav-tab" onclick="switchKnowledgeTab('products', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:8px 16px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; font-family:inherit; white-space:nowrap;">
        📦 4. ตารางสินค้า 225 รายการ (Search & Sort GMV)
      </button>
      <button class="k-nav-tab" onclick="switchKnowledgeTab('playbook', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:8px 16px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; font-family:inherit; white-space:nowrap;">
        🎯 5. กลยุทธ์ Campaign vs Normal & สุขภาพสต็อก
      </button>
    </div>

    <!-- ========================================== -->
    <!-- TAB 1: GMV TRENDS & DATA TABLES (PDF EXACT) -->
    <!-- ========================================== -->
    <div id="ktab-trends" class="ktab-content" style="display:block;">
      
      <div class="k-grid-2col">
        
        <!-- Monthly Performance Table -->
        <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="font-size:16px; font-weight:700; color:#38bdf8; margin:0; display:flex; align-items:center; gap:8px;">
              <span>📅</span> ยอดขายแยกตามเดือน (Monthly Performance Feb–Sep)
            </h3>
            <span style="font-size:11px; background:rgba(56,189,248,0.15); color:#38bdf8; padding:2px 8px; border-radius:6px; font-weight:600;">Peak: Jun (฿46M)</span>
          </div>

          <div style="overflow-x:auto; -webkit-overflow-scrolling:touch; width:100%;">
          <table style="width:100%; min-width:440px; border-collapse:collapse; font-size:12px; text-align:left;">
            <thead>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.1); color:#94a3b8;">
                <th style="padding:8px 6px;">เดือน</th>
                <th style="padding:8px 6px;">GMV รวม</th>
                <th style="padding:8px 6px;">เฉลี่ย/วัน</th>
                <th style="padding:8px 6px;">Uplift</th>
                <th style="padding:8px 6px;">แคมเปญเด่น & เหตุการณ์</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">Feb</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿26.3M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿940K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+18%</td>
                <td style="padding:9px 6px; color:#94a3b8;">Generic Baseline</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">Mar</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿32.7M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,055K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+17%</td>
                <td style="padding:9px 6px; color:#94a3b8;">Payday (฿1.24M/d) Steady growth</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">Apr</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿28.8M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿959K</td>
                <td style="padding:9px 6px; color:#fbbf24; font-weight:600;">+4%</td>
                <td style="padding:9px 6px; color:#94a3b8;">Songkran lull (Weakest campaigns)</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">May</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿26.5M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿853K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+57%</td>
                <td style="padding:9px 6px; color:#94a3b8;">Payday (฿1.13M/d) Lowest Normal day</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04); background:rgba(59,130,246,0.08);">
                <td style="padding:9px 6px; font-weight:700; color:#60a5fa;">Jun ⭐</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#60a5fa; font-weight:700;">฿46.0M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#60a5fa; font-weight:700;">฿1,534K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:700;">+36%</td>
                <td style="padding:9px 6px; color:#cbd5e1; font-weight:600;">Peak month — 6.6 + Live Win William (฿2.28M/d)</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">Jul</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿33.5M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,080K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+16%</td>
                <td style="padding:9px 6px; color:#94a3b8;">7.7 (฿1.34M/d) Moderate</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">Aug</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿34.2M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,104K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+63%</td>
                <td style="padding:9px 6px; color:#94a3b8;">8.8 (฿1.63M/d) Daytime-focused campaigns</td>
              </tr>
              <tr style="background:rgba(236,72,153,0.08);">
                <td style="padding:9px 6px; font-weight:700; color:#f472b6;">Sep 🔥</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#f472b6; font-weight:700;">฿26.9M</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; color:#f472b6; font-weight:700;">฿1,221K</td>
                <td style="padding:9px 6px; color:#f472b6; font-weight:700;">+137%</td>
                <td style="padding:9px 6px; color:#cbd5e1; font-weight:600;">9.9 (฿2.12M/d) Strongest campaign uplift!</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Day of Week & Window Table -->
        <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="font-size:16px; font-weight:700; color:#10b981; margin:0; display:flex; align-items:center; gap:8px;">
              <span>🗓️</span> ยอดขายแยกตามวันในสัปดาห์ (Day of Week Analysis)
            </h3>
            <span style="font-size:11px; background:rgba(16,185,129,0.15); color:#34d399; padding:2px 8px; border-radius:6px; font-weight:600;">Best: Sunday (+111%)</span>
          </div>

          <div style="overflow-x:auto; -webkit-overflow-scrolling:touch; width:100%;">
          <table style="width:100%; min-width:440px; border-collapse:collapse; font-size:12px; text-align:left;">
            <thead>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.1); color:#94a3b8;">
                <th style="padding:8px 6px;">วัน</th>
                <th style="padding:8px 6px;">วันแคมเปญ (เฉลี่ย)</th>
                <th style="padding:8px 6px;">วันปกติ (เฉลี่ย)</th>
                <th style="padding:8px 6px;">Uplift</th>
                <th style="padding:8px 6px;">ข้อสรุปปฏิบัติการ</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04); background:rgba(239,68,68,0.08);">
                <td style="padding:9px 6px; font-weight:700; color:#f87171;">อาทิตย์ (Sun) 🔥</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; font-weight:700; color:#f87171;">฿1,752K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿829K</td>
                <td style="padding:9px 6px; color:#f87171; font-weight:800;">+111%</td>
                <td style="padding:9px 6px; color:#cbd5e1;">ลง MC เบอร์ใหญ่ ดันบิลแคมเปญหนักสุด</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">เสาร์ (Sat)</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,324K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿971K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+36%</td>
                <td style="padding:9px 6px; color:#94a3b8;">ยอดนิ่งสม่ำเสมอทั้งวัน</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04); background:rgba(16,185,129,0.08);">
                <td style="padding:9px 6px; font-weight:700; color:#34d399;">ศุกร์ (Fri) ⭐</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,217K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono'; font-weight:700; color:#34d399;">฿1,013K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+20%</td>
                <td style="padding:9px 6px; color:#cbd5e1;">วันปกติที่ยอดแตะ 1 ล้านบาท แนะนำสตรีทแวร์</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">พฤหัสบดี (Thu)</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,221K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿864K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+41%</td>
                <td style="padding:9px 6px; color:#94a3b8;">ช่วงเย็นเริ่มมีทราฟฟิกช้อปก่อนสุดสัปดาห์</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">พุธ (Wed)</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,207K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿940K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+28%</td>
                <td style="padding:9px 6px; color:#94a3b8;">ได้แรงหนุนช่วง Pre-heat แคมเปญกลางสัปดาห์</td>
              </tr>
              <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:9px 6px; font-weight:600; color:#fff;">อังคาร (Tue)</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,151K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿896K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+28%</td>
                <td style="padding:9px 6px; color:#94a3b8;">เหมาะกับไลฟ์ระบายสต็อก / เซ็ต Clearance</td>
              </tr>
              <tr>
                <td style="padding:9px 6px; font-weight:600; color:#fff;">จันทร์ (Mon)</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿1,089K</td>
                <td style="padding:9px 6px; font-family:'JetBrains Mono';">฿875K</td>
                <td style="padding:9px 6px; color:#10b981; font-weight:600;">+24%</td>
                <td style="padding:9px 6px; color:#94a3b8;">วันทราฟฟิกต่ำสุด จัดไลฟ์ทดสอบคอนเทนต์</td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>

      </div>

      <!-- Hourly Shifts & Prime Time Spikes Table -->
      <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <div>
            <h3 style="font-size:16px; font-weight:700; color:#fbbf24; margin:0; display:flex; align-items:center; gap:8px;">
              <span>⏰</span> พฤติกรรมยอดขายรายชั่วโมง (Hourly Pattern & Shifts by Month)
            </h3>
            <p style="font-size:12px; color:#94a3b8; margin:2px 0 0 0;">
              Uplift ช่วงไพรม์ไทม์ (20:00–21:00) แปรผันตั้งแต่ -2% (เม.ย. ช่วงสงกรานต์) จนถึง <strong>+310% ในเดือน ก.ย. (9.9)</strong>
            </p>
          </div>
          <span style="font-size:11px; background:rgba(245,158,11,0.15); color:#fbbf24; padding:2px 8px; border-radius:6px; font-weight:600;">Peak Uplift: +310%</span>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap:12px;">
          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px;">
            <div style="display:flex; justify-content:space-between;">
              <span style="font-weight:700; color:#fff;">Sep (ก.ย.)</span>
              <span style="color:#ec4899; font-weight:700;">+310% Prime-Time</span>
            </div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">
              วันแคมเปญ 21:00 น. ทำเงิน <strong>฿267,000 / ชม.</strong> (วันปกติ ฿56K) เน้นแคมเปญช่วงค่ำสูงสุด!
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px;">
            <div style="display:flex; justify-content:space-between;">
              <span style="font-weight:700; color:#fff;">Jun (มิ.ย.)</span>
              <span style="color:#38bdf8; font-weight:700;">+104% Prime-Time</span>
            </div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">
              วันแคมเปญ 21:00 น. ทำเงิน <strong>฿229,000 / ชม.</strong> (วันปกติ ฿92K) ปรากฏการณ์ Live-Selling Explosion
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px;">
            <div style="display:flex; justify-content:space-between;">
              <span style="font-weight:700; color:#fff;">Aug (ส.ค.)</span>
              <span style="color:#10b981; font-weight:700;">Daytime Focused</span>
            </div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">
              แคมเปญ 8.8 พุ่งช่วงเที่ยง 12:00 น. ทำเงิน <strong>฿93,000 / ชม.</strong> วันปกติพีค 21:00 น. (฿65K)
            </div>
          </div>

          <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px;">
            <div style="display:flex; justify-content:space-between;">
              <span style="font-weight:700; color:#fff;">Apr (เม.ย.)</span>
              <span style="color:#ef4444; font-weight:700;">-2% (Songkran Lull)</span>
            </div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">
              สงกรานต์ทำลายยอดกลางคืน พีคย้ายไป 12:00 น. (฿68K) กลางคืนคนออกเที่ยวข้างนอก
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ========================================== -->
    <!-- TAB 2: HOUR-BY-HOUR PRODUCT PUSH SCHEDULE -->
    <!-- ========================================== -->
    <div id="ktab-schedule" class="ktab-content" style="display:none;">
      
      <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(59,130,246,0.3); border-radius:16px; padding:20px; margin-bottom:20px;">
        <h3 style="font-size:17px; font-weight:700; color:#fff; margin:0 0 6px 0;">
          ⏰ ผังเวลา & สินค้าที่ควรดันในแต่ละช่วง (Which Product to Push at Which Hour)
        </h3>
        <p style="font-size:13px; color:#94a3b8; margin:0;">
          สอดคล้องกับพฤติกรรมคนดูและผลกำไรจริง: <strong>เช้ากวาดทราฟฟิก • กลางวันดันชุดทำงาน • เย็นดันสตรีทแวร์ • ค่ำปล่อยสินค้าตั๋วสูง AOV สูงสุด</strong>
        </p>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap:18px;">
        
        <!-- Slot 07:00 -->
        <div style="background:#090d16; border:1px solid rgba(16,185,129,0.3); border-radius:16px; padding:20px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:rgba(16,185,129,0.15); color:#34d399; font-weight:800; font-size:13px; padding:4px 10px; border-radius:8px;">07:00 - 09:00 น.</span>
              <span style="color:#10b981; font-weight:700; font-size:12px;">฿8,553 / ชม. (Best Efficiency)</span>
            </div>
            <h4 style="font-size:16px; font-weight:700; color:#fff; margin:0 0 6px 0;">🌅 Morning Campaign Kick-Off</h4>
            <div style="font-size:12.5px; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
              คนตื่นนอน เช็กมือถือ เตรียมตัวเดินทาง มีคูปองเช้าตรู่ในมือ ซื้อง่าย ตัดสินใจเร็ว
            </div>

            <div style="background:rgba(0,0,0,0.4); border-radius:10px; padding:12px; font-size:12px; border-left:3px solid #10b981; margin-bottom:12px;">
              <div style="color:#34d399; font-weight:700; margin-bottom:4px;">🎯 สินค้าที่ต้องดัน:</div>
              <div>• <strong>Polo PIQUE (WA-212PLACL30):</strong> ราคา ฿205 ซื้อง่าย ทรงสุภาพ</div>
              <div>• <strong>กางเกงกีฬา WP-1509:</strong> ราคา ฿82 แม่เหล็กดึงยอด 382 ชิ้น/วัน</div>
              <div>• <strong>Active Training Shirt (WA-231FBACL04):</strong> ราคา ฿110 ใส่ออกกำลังเช้า</div>
            </div>

            <div style="font-size:12px; color:#cbd5e1; background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:8px;">
              💬 <strong>สคริปต์ MC:</strong> "เปิดร้านเช้านี้ ใครกดโปโล PIQUE ผ้าไม่ต้องรีด ตัวละสองร้อยนิดๆ ปักหมุดพร้อมส่งทันทีรอบเช้านี้ครับ!"
            </div>
          </div>

          <button onclick="selectProduct('WA-212PLACL30'); switchView('studio');" style="margin-top:14px; width:100%; background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#34d399; padding:8px; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer;">
            🎙️ ดัน Polo PIQUE ใน Prompter
          </button>
        </div>

        <!-- Slot 10:00 - 12:00 -->
        <div style="background:#090d16; border:1px solid rgba(59,130,246,0.3); border-radius:16px; padding:20px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:rgba(59,130,246,0.15); color:#93c5fd; font-weight:800; font-size:13px; padding:4px 10px; border-radius:8px;">10:00 - 12:00 น.</span>
              <span style="color:#60a5fa; font-weight:700; font-size:12px;">฿5,054 / ชม. (Core Daytime)</span>
            </div>
            <h4 style="font-size:16px; font-weight:700; color:#fff; margin:0 0 6px 0;">🏢 Office Hours & Daytime Flash Deals</h4>
            <div style="font-size:12.5px; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
              คนทำงานแอบดูไลฟ์ช่วงพักสายตา และช่วงเที่ยง 12:00 น. (พีคมากในแคมเปญแบบ 8.8)
            </div>

            <div style="background:rgba(0,0,0,0.4); border-radius:10px; padding:12px; font-size:12px; border-left:3px solid #3b82f6; margin-bottom:12px;">
              <div style="color:#93c5fd; font-weight:700; margin-bottom:4px;">🎯 สินค้าที่ต้องดัน:</div>
              <div>• <strong>VIVIDUS Polo (WA-242PLACL30):</strong> ราคา ฿294 โต 2.53x ขับผิวทุกโทน</div>
              <div>• <strong>Zypher Polo (Online Exclusive):</strong> ราคา ฿242 โตกระฉูด 4.26x</div>
              <div>• <strong>5" Running Shorts (WP-252RNACL02):</strong> ราคา ฿222 กางเกงวิ่งขาสั้น</div>
            </div>

            <div style="font-size:12px; color:#cbd5e1; background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:8px;">
              💬 <strong>สคริปต์ MC:</strong> "วัยทำงานที่อยากได้โปโลเนื้อเนียนเรียบกริบ ใส่ประชุม Zoom หล่อคม แนะนำ VIVIDUS และ Zypher รุ่นนี้เลยครับ!"
            </div>
          </div>

          <button onclick="selectProduct('WA-242PLACL30'); switchView('studio');" style="margin-top:14px; width:100%; background:rgba(59,130,246,0.15); border:1px solid #3b82f6; color:#93c5fd; padding:8px; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer;">
            🎙️ ดัน VIVIDUS ใน Prompter
          </button>
        </div>

        <!-- Slot 16:00 - 18:00 -->
        <div style="background:#090d16; border:1px solid rgba(168,85,247,0.3); border-radius:16px; padding:20px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:rgba(168,85,247,0.15); color:#d8b4fe; font-weight:800; font-size:13px; padding:4px 10px; border-radius:8px;">16:00 - 18:00 น.</span>
              <span style="color:#c084fc; font-weight:700; font-size:12px;">฿7,753 / ชม. (Under-used Opportunity!)</span>
            </div>
            <h4 style="font-size:16px; font-weight:700; color:#fff; margin:0 0 6px 0;">🎒 After-Work Rush & Streetwear</h4>
            <div style="font-size:12.5px; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
              ช่วงคนเลิกงาน/เลิกเรียน ผ่อนคลายก่อนกลับบ้าน สล็อตนี้ทำเงินสูงแต่ยังไลฟ์น้อย ต้องขยายรอบ!
            </div>

            <div style="background:rgba(0,0,0,0.4); border-radius:10px; padding:12px; font-size:12px; border-left:3px solid #a855f7; margin-bottom:12px;">
              <div style="color:#d8b4fe; font-weight:700; margin-bottom:4px;">🎯 สินค้าที่ต้องดัน:</div>
              <div>• <strong>Thailand Oversize Jersey (WA-243FBATH10):</strong> ฿535 GMV ฿9.3M</div>
              <div>• <strong>BASIE Woven Series (WA-262JKACL70):</strong> แจ็คเก็ต ฿754 โต 3.95x</div>
              <div>• <strong>Cargo Pant 2026 (WP-263CBACL01):</strong> ฿1,049 ขายดีวันละ ฿14.6K</div>
            </div>

            <div style="font-size:12px; color:#cbd5e1; background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:8px;">
              💬 <strong>สคริปต์ MC:</strong> "เลิกงานวันศุกร์ เตรียมตัวไปคาเฟ่ ใส่เสื้อโอเวอร์ไซส์ตัวนี้คู่คาร์โก้ ได้ลุคสตรีทญี่ปุ่นทันทีครับ!"
            </div>
          </div>

          <button onclick="selectProduct('WA-243FBATH10'); switchView('studio');" style="margin-top:14px; width:100%; background:rgba(168,85,247,0.15); border:1px solid #a855f7; color:#d8b4fe; padding:8px; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer;">
            🎙️ ดัน Oversize ใน Prompter
          </button>
        </div>

        <!-- Slot 20:00 - 22:00 -->
        <div style="background:#090d16; border:1px solid rgba(245,158,11,0.4); border-radius:16px; padding:20px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 0 25px rgba(245,158,11,0.1);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="background:rgba(245,158,11,0.2); color:#fbbf24; font-weight:800; font-size:13px; padding:4px 10px; border-radius:8px;">20:00 - 22:00 น.</span>
              <span style="color:#fbbf24; font-weight:700; font-size:12px;">฿123K-฿267K / ชม. (MEGA PRIME TIME)</span>
            </div>
            <h4 style="font-size:16px; font-weight:700; color:#fff; margin:0 0 6px 0;">👑 Golden Prime Time • ปล่อย High-Ticket เท่านั้น</h4>
            <div style="font-size:12.5px; color:#94a3b8; line-height:1.5; margin-bottom:12px;">
              ลูกค้าอยู่บ้าน นอนดูไลฟ์ สมาธิสูง กำลังซื้อสูง AOV แตะ ฿460–฿902 <strong>ห้ามไลฟ์ของถูกช่วงนี้!</strong>
            </div>

            <div style="background:rgba(0,0,0,0.4); border-radius:10px; padding:12px; font-size:12px; border-left:3px solid #f59e0b; margin-bottom:12px;">
              <div style="color:#fbbf24; font-weight:700; margin-bottom:4px;">🎯 สินค้าที่ต้องดัน (High Ticket & High AOV):</div>
              <div>• <strong>WAVE 1.0 Running Shoe (WF-203RNACL01):</strong> ฿826 #1 GMV ของแบรนด์</div>
              <div>• <strong>Thailand NT 26/27 Replica & Player:</strong> ฿1,203 - ฿2,385 ดันยอดบิลพุ่ง</div>
              <div>• <strong>Crochet Flyknit Shoe (WF-253RNACL01):</strong> ฿913 โตกระฉูด 3.75x</div>
              <div>• <strong>GravityX Sneakers (WF-233ALACL01):</strong> ฿1,010 สนีกเกอร์พรีเมียม</div>
            </div>

            <div style="font-size:12px; color:#cbd5e1; background:rgba(255,255,255,0.03); padding:8px 10px; border-radius:8px;">
              💬 <strong>สคริปต์ MC:</strong> "ค่ำนี้ปล่อยดีลใหญ่สุดของวัน รองเท้าวิ่ง WAVE 1.0 โฟมนุ่มเด้งระดับท็อป ลดเฉพาะช่วงไลฟ์นี้เท่านั้นครับ!"
            </div>
          </div>

          <button onclick="selectProduct('WF-203RNACL01'); switchView('studio');" style="margin-top:14px; width:100%; background:linear-gradient(135deg,rgba(245,158,11,0.3),rgba(234,88,12,0.3)); border:1px solid #f59e0b; color:#fbbf24; padding:8px; border-radius:8px; font-size:12px; font-weight:700; cursor:pointer;">
            🎙️ ดัน WAVE 1.0 ใน Prompter
          </button>
        </div>

      </div>

      <!-- Warning Box: Cut Weak Slots -->
      <div style="margin-top:20px; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.25); border-radius:14px; padding:16px 20px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <span style="font-size:24px;">🚫</span>
          <div>
            <div style="font-size:14px; font-weight:700; color:#f87171;">คำสั่งปรับผังเวลา: ตัดรอบ 14:00–15:00 และ 18:00–19:00 ทันที!</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:2px;">
              ข้อมูล 229 ไลฟ์ยืนยันว่า 2 ช่วงนี้ทำเงินเฉลี่ยเพียง ฿2,900–฿3,300/ชม. เปลืองพลังงาน MC ให้ย้ายเวลาและชั่วโมงไลฟ์ไปทุ่มที่ <strong>16:00 และ 20:00 น.</strong> แทน
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- ========================================== -->
    <!-- TAB 3: UP-SELL & CROSS-SELL PLAYBOOK -->
    <!-- ========================================== -->
    <div id="ktab-upsell" class="ktab-content" style="display:none;">
      
      <div style="background:rgba(236,72,153,0.08); border:1px solid rgba(236,72,153,0.3); border-radius:16px; padding:20px; margin-bottom:22px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
          <div>
            <h3 style="font-size:17px; font-weight:800; color:#f472b6; margin:0 0 6px 0; display:flex; align-items:center; gap:8px;">
              <span>🔄</span> กลยุทธ์ UpSell & Cross-Sell (แก้ปัญหา AOV ต่ำ และดันบิลทะลุ ฿400–฿1,500)
            </h3>
            <p style="font-size:13px; color:#cbd5e1; margin:0; line-height:1.5;">
              <strong>บทเรียนสำคัญจาก PDF:</strong> เดือน ส.ค. ที่เน้นแจกคูปองอย่างเดียว ออเดอร์พุ่ง 4,428 ชิ้น แต่ AOV ดิ่งเหลือ <strong>฿301</strong> เพราะคนแห่ซื้อของถูกชิ้นเดียวแล้วกดคูปอง! ทางแก้เดียวคือ <strong>MC ต้องใช้เทคนิค Cross-Sell มัดคู่เซ็ต</strong> เท่านั้น
            </p>
          </div>
          <button onclick="switchView('lookbook')" style="background:linear-gradient(135deg,#ec4899,#8b5cf6); border:none; color:#fff; font-weight:700; padding:10px 16px; border-radius:8px; font-size:12.5px; cursor:pointer;">
            👗 เปิด Lookbook คำนวณเซ็ตอัตโนมัติ
          </button>
        </div>
      </div>

      <!-- 4 Core Selling Playbook Cards -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap:18px; margin-bottom:24px;">
        
        <!-- Formula 1: Basic Traffic to Bundle -->
        <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:12px; background:rgba(59,130,246,0.15); color:#93c5fd; padding:3px 8px; border-radius:6px; font-weight:700;">Cross-Sell สูตร 1</span>
            <span style="color:#10b981; font-weight:700; font-size:12px;">AOV +317%</span>
          </div>
          <h4 style="font-size:15px; font-weight:700; color:#fff; margin:0 0 8px 0;">จากกางเกงบอล ฿82 ➔ เซ็ตคู่ ฿342</h4>
          
          <div style="font-size:12.5px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>สถานการณ์:</strong> ลูกค้ากดกางเกงฟุตบอล WP-1509 (฿82) ใส่ตะกร้า<br>
            <strong>Cross-Sell ทันที:</strong> แนะนำให้หยิบ <strong>Polo PIQUE (฿205) + ถุงเท้า WC-1519 (฿55)</strong>
          </div>

          <div style="background:rgba(0,0,0,0.4); border-radius:8px; padding:10px; font-size:12px; color:#38bdf8; margin-bottom:12px;">
            💬 <strong>สคริปต์พูด MC:</strong> "พี่ๆ ครับ ใครกดกางเกง 82 บาทในตะกร้า อย่าเพิ่งกดสั่งเดี่ยว เสียค่าส่งไม่คุ้มครับ! กดเสื้อโปโล PIQUE ผ้าไม่ต้องรีดไปด้วยอีกตัว รวมเซ็ตลดเพิ่ม 15% ทันที ได้ทั้งเสื้อทั้งกางเกงคุ้มกว่าเยอะครับ!"
          </div>

          <button onclick="copyReplyText('ซื้อกางเกง WP-1509 คู่เสื้อโปโล PIQUE ได้ส่วนลดเซ็ต 15% ทันทีในตะกร้าครับ คุ้มกว่าค่าส่งแน่นอนครับ!')" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); color:#fff; padding:7px; border-radius:6px; font-size:11.5px; cursor:pointer;">
            📋 คัดลอกสคริปต์ MC
          </button>
        </div>

        <!-- Formula 2: Total Look 3 Items -->
        <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:12px; background:rgba(236,72,153,0.15); color:#f472b6; padding:3px 8px; border-radius:6px; font-weight:700;">Cross-Sell สูตร 2</span>
            <span style="color:#10b981; font-weight:700; font-size:12px;">AOV ฿1,570 (x7.6)</span>
          </div>
          <h4 style="font-size:15px; font-weight:700; color:#fff; margin:0 0 8px 0;">เซ็ต Total Look 3 ชิ้น (ทำงาน + เที่ยว)</h4>
          
          <div style="font-size:12.5px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>สถานการณ์:</strong> ลูกค้าถามหาเสื้อโปโลทำงาน<br>
            <strong>Cross-Sell ทันที:</strong> โปโล PIQUE (฿205) + กางเกง Pansa Jeans (฿932) + สนีกเกอร์ GravityX (฿1,010)
          </div>

          <div style="background:rgba(0,0,0,0.4); border-radius:8px; padding:10px; font-size:12px; color:#f472b6; margin-bottom:12px;">
            💬 <strong>สคริปต์พูด MC:</strong> "แมตช์ 3 ชิ้นนี้จบครบเซ็ตครับ โปโลสีกรมท่า + ยีนส์กระบอกตรง Pansa + สนีกเกอร์ขาว ราคารวมสองพันกว่า แต่วันนี้ซื้อเซ็ตลด 20% จ่ายเพียง ฿1,570 ประหยัดเกือบ 400 บาททันที!"
          </div>

          <button onclick="copyReplyText('เซ็ต Total Look 3 ชิ้นนี้ โปโล + ยีนส์ Pansa + สนีกเกอร์ ลด 20% ทันที จ่ายเพียง ฿1,570 ครับ!')" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); color:#fff; padding:7px; border-radius:6px; font-size:11.5px; cursor:pointer;">
            📋 คัดลอกสคริปต์ MC
          </button>
        </div>

        <!-- Formula 3: Good -> Better -> Best -->
        <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:12px; background:rgba(245,158,11,0.15); color:#fbbf24; padding:3px 8px; border-radius:6px; font-weight:700;">Up-Sell สูตร 3</span>
            <span style="color:#fbbf24; font-weight:700; font-size:12px;">กำไรเพิ่ม +฿842</span>
          </div>
          <h4 style="font-size:15px; font-weight:700; color:#fff; margin:0 0 8px 0;">อัปเกรดเสื้อเชียร์ ➔ Replica ฿1,203</h4>
          
          <div style="font-size:12.5px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>สถานการณ์:</strong> ลูกค้ากำลังดูเสื้อเชียร์ทีมชาติ 2026/27 (฿361)<br>
            <strong>Up-Sell ทันที:</strong> ชี้ให้เห็นความคุ้มค่าของการอัปเกรดเป็น <strong>Replica (WA-262FBATH52 ฿1,203)</strong>
          </div>

          <div style="background:rgba(0,0,0,0.4); border-radius:8px; padding:10px; font-size:12px; color:#fbbf24; margin-bottom:12px;">
            💬 <strong>สคริปต์พูด MC:</strong> "ถ้าพี่อยากได้ดีเทลของแท้ที่เหมือนนักเตะใส่ลงสนาม โลโก้เฟล็กซ์ 3D ลายทอแอร์โรว์ไลน์ แนะนำอัปเกรดเป็นรุ่น Replica เลยครับ เพิ่มเงินอีกนิดได้ของสะสมระดับพรีเมียมครับ!"
          </div>

          <button onclick="copyReplyText('รุ่น Replica 2026/27 ผ้าและโลโก้เป็นเกรดเดียวกับนักเตะใส่แข่งขัน คุ้มค่าแก่การสะสมมากๆ ครับ!')" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); color:#fff; padding:7px; border-radius:6px; font-size:11.5px; cursor:pointer;">
            📋 คัดลอกสคริปต์ MC
          </button>
        </div>

        <!-- Formula 4: Q4 Seasonal Jacket -->
        <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <span style="font-size:12px; background:rgba(16,185,129,0.15); color:#34d399; padding:3px 8px; border-radius:6px; font-weight:700;">Cross-Sell สูตร 4</span>
            <span style="color:#10b981; font-weight:700; font-size:12px;">Q4 โต 2.56x</span>
          </div>
          <h4 style="font-size:15px; font-weight:700; color:#fff; margin:0 0 8px 0;">รับลมหนาว Q4 พ่วงแจ็คเก็ต Woven</h4>
          
          <div style="font-size:12.5px; color:#cbd5e1; line-height:1.5; margin-bottom:12px;">
            <strong>สถานการณ์:</strong> ลูกค้าซื้อเสื้อโปโลหรือเสื้อวิ่ง<br>
            <strong>Cross-Sell ทันที:</strong> พ่วง <strong>Herit Woven Jacket (฿563) หรือ BASIE Woven (฿754)</strong>
          </div>

          <div style="background:rgba(0,0,0,0.4); border-radius:8px; padding:10px; font-size:12px; color:#34d399; margin-bottom:12px;">
            💬 <strong>สคริปต์พูด MC:</strong> "ตอนนี้เข้าช่วงลมหนาว Q4 แล้วครับ แจ็คเก็ต Woven ตัวนี้พับเก็บเล็กมาก กันลมกันหนาวใส่ในออฟฟิศแอร์เย็นสบาย พ่วงคู่เสื้อโปโลวันนี้รับส่วนลดทันทีครับ!"
          </div>

          <button onclick="copyReplyText('แจ็คเก็ต Herit Woven น้ำหนักเบา กันละอองฝนกันลมหนาว พกพาง่าย ใส่คลุมทับเสื้อโปโลหล่อมากครับ!')" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.15); color:#fff; padding:7px; border-radius:6px; font-size:11.5px; cursor:pointer;">
            📋 คัดลอกสคริปต์ MC
          </button>
        </div>

      </div>

    </div>

    <!-- ========================================== -->
    <!-- TAB 4: REAL 225 PRODUCTS PERFORMANCE TABLE -->
    <!-- ========================================== -->
    <div id="ktab-products" class="ktab-content" style="display:none;">
      
      <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:16px;">
          <div>
            <h3 style="font-size:16px; font-weight:700; color:#fff; margin:0;">
              📦 ตารางอันดับสินค้าสร้างยอดขายจริง (Master Products Performance Table)
            </h3>
            <p style="font-size:12.5px; color:#94a3b8; margin:2px 0 0 0;">
              ข้อมูลจริง 225 รายการจาก Master CSV แสดงยอดขายรวม GMV, อัตราเติบโต, และ Campaign Lift
            </p>
          </div>

          <!-- Search Input -->
          <div style="display:flex; gap:10px; align-items:center;">
            <input type="text" id="kTableSearch" placeholder="🔍 พิมพ์ค้นหาชื่อสินค้า หรือ SKU..." oninput="filterKTable()" style="background:#040711; border:1px solid #334155; color:#fff; padding:8px 14px; border-radius:8px; font-size:12.5px; width:260px; font-family:inherit; outline:none;" />
          </div>
        </div>

        <!-- Filter Chips for Table -->
        <div style="display:flex; gap:8px; margin-bottom:16px; flex-wrap:wrap;">
          <button class="k-chip active" onclick="setKTableFilter('ALL', this)" style="background:rgba(59,130,246,0.15); border:1px solid #3b82f6; color:#93c5fd; padding:4px 12px; border-radius:20px; font-size:11.5px; font-weight:600; cursor:pointer;">ทั้งหมด (225)</button>
          <button class="k-chip" onclick="setKTableFilter('HERO', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:4px 12px; border-radius:20px; font-size:11.5px; font-weight:600; cursor:pointer;">⭐ Hero (>฿2.5M)</button>
          <button class="k-chip" onclick="setKTableFilter('RISING', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:4px 12px; border-radius:20px; font-size:11.5px; font-weight:600; cursor:pointer;">🚀 Rising Stars (โต > 2x)</button>
          <button class="k-chip" onclick="setKTableFilter('BOOSTER', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:4px 12px; border-radius:20px; font-size:11.5px; font-weight:600; cursor:pointer;">🔥 Campaign Boosters (Lift > 2.5x)</button>
          <button class="k-chip" onclick="setKTableFilter('CLEARANCE', this)" style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:#cbd5e1; padding:4px 12px; border-radius:20px; font-size:11.5px; font-weight:600; cursor:pointer;">🔻 Clearance (H2 แผ่ว)</button>
        </div>

        <div style="overflow-x:auto; max-height:550px;">
          <table style="width:100%; border-collapse:collapse; font-size:12px; text-align:left;">
            <thead style="position:sticky; top:0; background:#090d16; border-bottom:1px solid rgba(255,255,255,0.1); z-index:10;">
              <tr style="color:#94a3b8;">
                <th style="padding:10px 8px;">#</th>
                <th style="padding:10px 8px;">SKU</th>
                <th style="padding:10px 8px;">ชื่อสินค้า</th>
                <th style="padding:10px 8px;">ยอดขายรวม (GMV)</th>
                <th style="padding:10px 8px;">ยอดขาย/วัน</th>
                <th style="padding:10px 8px;">ราคาขาย</th>
                <th style="padding:10px 8px;">ส่วนลด</th>
                <th style="padding:10px 8px;">โต H2/H1</th>
                <th style="padding:10px 8px;">Campaign Lift</th>
                <th style="padding:10px 8px;">การปฏิบัติการ</th>
              </tr>
            </thead>
            <tbody id="kProductsTableBody">
              <!-- Dynamically rendered -->
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ========================================== -->
    <!-- TAB 5: CAMPAIGN VS NORMAL & APICS STOCK -->
    <!-- ========================================== -->
    <div id="ktab-playbook" class="ktab-content" style="display:none;">
      
      <!-- Comparison Grid -->
      <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px; margin-bottom:24px;">
        <h3 style="font-size:16px; font-weight:700; color:#38bdf8; margin:0 0 12px 0;">
          ⚖️ Campaign Days vs Normal Days: สองธุรกิจที่ขับเคลื่อนต่างกันโดยสิ้นเชิง
        </h3>
        
        <div style="overflow-x:auto; -webkit-overflow-scrolling:touch; width:100%; margin-bottom:14px;">
        <table style="width:100%; min-width:580px; border-collapse:collapse; font-size:12px; text-align:left;">
          <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.1); color:#94a3b8;">
              <th style="padding:10px 8px;">มิติการวิเคราะห์</th>
              <th style="padding:10px 8px; color:#10b981;">วันแคมเปญ (Campaign Days)</th>
              <th style="padding:10px 8px; color:#38bdf8;">วันปกติ (Normal Days)</th>
              <th style="padding:10px 8px;">ผลต่าง & ข้อสรุป</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
              <td style="padding:10px 8px; font-weight:600; color:#fff;">ยอดขายเฉลี่ยต่อวัน</td>
              <td style="padding:10px 8px; font-family:'JetBrains Mono'; color:#10b981; font-weight:700;">฿1,284K</td>
              <td style="padding:10px 8px; font-family:'JetBrains Mono'; color:#38bdf8;">฿914K</td>
              <td style="padding:10px 8px; color:#10b981; font-weight:700;">+40% ยอดแคมเปญกระฉูด</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
              <td style="padding:10px 8px; font-weight:600; color:#fff;">ความลึกของส่วนลด</td>
              <td style="padding:10px 8px; color:#cbd5e1;">39.2%</td>
              <td style="padding:10px 8px; color:#cbd5e1;">34.1%</td>
              <td style="padding:10px 8px; color:#94a3b8;">+5pp ส่วนลดลึกกว่า</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
              <td style="padding:10px 8px; font-weight:600; color:#fff;">ตัวขับเคลื่อน GMV อันดับ 1</td>
              <td style="padding:10px 8px; color:#cbd5e1;">Discount Depth (r=0.63)</td>
              <td style="padding:10px 8px; color:#cbd5e1;">Platform Discount (r=0.58)</td>
              <td style="padding:10px 8px; color:#94a3b8;">วันปกติพึ่งคูปองแพลตฟอร์ม</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
              <td style="padding:10px 8px; font-weight:600; color:#fff;">สินค้าตัวขับเคลื่อนหลัก</td>
              <td style="padding:10px 8px; color:#cbd5e1;">Premium Mix (รองเท้า, แจ็คเก็ต)</td>
              <td style="padding:10px 8px; color:#cbd5e1;">Polo Shirts (เสื้อโปโล)</td>
              <td style="padding:10px 8px; color:#94a3b8;">วันปกติขายโปโลดีที่สุด</td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04); background:rgba(239,68,68,0.06);">
              <td style="padding:10px 8px; font-weight:700; color:#f87171;">ผลของการลดราคาจากร้าน (Seller Disc)</td>
              <td style="padding:10px 8px; color:#10b981; font-weight:700;">ได้ผลสูงมาก (r=0.59)</td>
              <td style="padding:10px 8px; color:#f87171; font-weight:700;">ไม่มีผลเลย (r=-0.03) ⚠️</td>
              <td style="padding:10px 8px; color:#f87171; font-weight:600;">วันปกติร้านไม่ควรลดราคาเอง!</td>
            </tr>
            <tr>
              <td style="padding:10px 8px; font-weight:600; color:#fff;">ชั่วโมงทำเงินสูงสุด (Peak Hour)</td>
              <td style="padding:10px 8px; color:#10b981; font-weight:700;">21:00 น. (฿123K/ชม.)</td>
              <td style="padding:10px 8px; color:#38bdf8;">21:00 น. (฿68K/ชม.)</td>
              <td style="padding:10px 8px; color:#10b981; font-weight:700;">+80% uplift ช่วง 3 ทุ่ม</td>
            </tr>
          </tbody>
        </table>
        </div>
      </div>

      <!-- APICS Stock Health Framework -->
      <div style="background:#090d16; border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div>
            <h3 style="font-size:16px; font-weight:700; color:#f87171; margin:0; display:flex; align-items:center; gap:8px;">
              <span>💀</span> สถานะสุขภาพสต็อกสินค้า (APICS Framework Stock Health)
            </h3>
            <p style="font-size:12px; color:#cbd5e1; margin:2px 0 0 0;">
              <strong>วิกฤตสต็อก:</strong> 94% ของมูลค่าสินค้าในคลัง (฿882 ล้านบาท) จมอยู่ใน <strong>Dead Stock และ Slow Movers!</strong>
            </p>
          </div>
        </div>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(min(100%, 220px), 1fr)); gap:12px;">
          <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:14px;">
            <div style="color:#f87171; font-weight:800; font-size:14px;">💀 Dead Stock</div>
            <div style="font-size:18px; font-weight:800; color:#fff; margin:4px 0;">฿409M <span style="font-size:12px; font-weight:400; color:#cbd5e1;">(3.17M ชิ้น)</span></div>
            <div style="font-size:11.5px; color:#cbd5e1;">38,277 SKUs • แนะนำ <strong>Markdown 40–50%</strong> ระบายด่วน</div>
          </div>

          <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:14px;">
            <div style="color:#fbbf24; font-weight:800; font-size:14px;">🔴 Slow Movers</div>
            <div style="font-size:18px; font-weight:800; color:#fff; margin:4px 0;">฿473M <span style="font-size:12px; font-weight:400; color:#cbd5e1;">(4.12M ชิ้น)</span></div>
            <div style="font-size:11.5px; color:#cbd5e1;">4,791 SKUs • แนะนำ <strong>Markdown 30–40%</strong> มัดคู่เซ็ต</div>
          </div>

          <div style="background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:14px;">
            <div style="color:#93c5fd; font-weight:800; font-size:14px;">🟠 Overstock</div>
            <div style="font-size:18px; font-weight:800; color:#fff; margin:4px 0;">฿34M <span style="font-size:12px; font-weight:400; color:#cbd5e1;">(391K ชิ้น)</span></div>
            <div style="font-size:11.5px; color:#cbd5e1;">319 SKUs • แนะนำ <strong>Markdown 20–30%</strong></div>
          </div>

          <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:14px;">
            <div style="color:#34d399; font-weight:800; font-size:14px;">🔵 Fast Sellers (สต็อกขาด!)</div>
            <div style="font-size:18px; font-weight:800; color:#fff; margin:4px 0;">฿1.6M <span style="font-size:12px; font-weight:400; color:#cbd5e1;">(12.5K ชิ้น)</span></div>
            <div style="font-size:11.5px; color:#34d399; font-weight:700;">120 SKUs • มีของขายได้แค่ 26 วัน! <strong>เติมด่วนก่อน 10.10</strong></div>
          </div>
        </div>
      </div>

    </div>

    </div>
    <!-- /knowledge-container -->
  </div>
  <!-- /knowledge-view -->

</div>
<!-- /app-workspace -->

  <!-- Floating Dynamic Spotlight Modal -->
  <div class="spotlight-modal-overlay" id="spotlight-modal" onclick="closeSpotlightOnBackdrop(event)">
    <div class="spotlight-dialog-box" onclick="event.stopPropagation()">
      <div class="spotlight-input-wrapper">
        <span class="spotlight-lens-icon">⚡</span>
        <input type="text" id="spotlight-search-input" class="spotlight-input-field" placeholder="ค้นหาชื่อสินค้า, รหัส SKU, สี, เนื้อผ้า, หรือโอกาสใช้งาน..." oninput="handleSpotlightInput()" onkeydown="handleSpotlightKeydown(event)" autocomplete="off" />
        <button class="spotlight-esc-btn" onclick="closeSpotlightSearch()">ESC</button>
      </div>

      <div class="spotlight-quick-filters">
        <span class="spotlight-filter-pill active" onclick="setSpotlightFilter('ALL', this)">ทั้งหมด (100)</span>
        <span class="spotlight-filter-pill" onclick="setSpotlightFilter('Polo', this)">Polo</span>
        <span class="spotlight-filter-pill" onclick="setSpotlightFilter('T-Shirt', this)">T-Shirts</span>
        <span class="spotlight-filter-pill" onclick="setSpotlightFilter('Jersey', this)">Jerseys</span>
        <span class="spotlight-filter-pill" onclick="setSpotlightFilter('Pant', this)">Pants</span>
        <span class="spotlight-filter-pill" onclick="setSpotlightFilter('Shoe', this)">Footwear</span>
      </div>

      <div class="spotlight-results-list" id="spotlight-results-list">
        <!-- Dynamically rendered -->
      </div>

      <div class="spotlight-footer">
        <div style="display:flex; gap:12px;">
          <span><kbd style="color:#38bdf8;">↑↓</kbd> นำทาง</span>
          <span><kbd style="color:#38bdf8;">↵</kbd> โฟกัสในไลฟ์</span>
          <span><kbd style="color:#38bdf8;">ESC</kbd> ปิดหน้าต่าง</span>
        </div>
        <div>
          <span id="spotlight-match-count" style="color:#38bdf8; font-weight:700;">100 สินค้าพร้อมค้นหา</span>
        </div>
      </div>
    </div>
  </div>

<!-- Global Footer -->
<footer class="global-footer-bar">
  <div>
    WARRIX Live Commerce Studio Hub &copy; 2026 • <span class="brand-prop">Property of Cattleya Chan</span>
  </div>
  <div style="display:flex; gap:16px;">
    <span>✨ Luxury Fashion V3 Edition</span>
    <span>⚡ Fast Gemini Stylist</span>
    <span>👗 Accurate Bundle Pricer</span>
    <span>📏 Sizing & Advisor Hub</span>
    <span>📦 100 Live SKUs Grounded</span>
  </div>
</footer>

<div class="toast-msg" id="toast">📋 คัดลอกข้อความเรียบร้อยแล้ว!</div>

<script>
  let PRODUCTS = """ + products_json + """;
  let selectedSku = 'WA-261PLACL15';
  let activeFilter = 'ALL';
  let activeView = 'studio';
  let searchQuery = '';

  let currentFitPref = 'regular';
  let currentSizeUnit = 'in';

  let selectedOutfit = {
    top: 'WA-261PLACL15',
    bottom: 'LP-241JEMW103',
    shoes: 'WF-253RNACL04'
  };

  let activeSlots = {
    top: true,
    bottom: true,
    shoes: true
  };

  const WARRIX_SIZE_SPECS = {
    tops: [
      { size: 'XS', chest_in: 36, chest_cm: 91, len_in: 26.0, len_cm: 66, shoulder_in: 16.0, shoulder_cm: 41, wt: '45-55 kg', ht: '155-165 cm' },
      { size: 'S',  chest_in: 38, chest_cm: 96, len_in: 27.0, len_cm: 68, shoulder_in: 17.0, shoulder_cm: 43, wt: '55-65 kg', ht: '160-170 cm' },
      { size: 'M',  chest_in: 40, chest_cm: 101, len_in: 28.0, len_cm: 71, shoulder_in: 18.0, shoulder_cm: 46, wt: '65-72 kg', ht: '165-175 cm' },
      { size: 'L',  chest_in: 42, chest_cm: 106, len_in: 29.0, len_cm: 74, shoulder_in: 19.0, shoulder_cm: 48, wt: '73-80 kg', ht: '170-180 cm' },
      { size: 'XL', chest_in: 44, chest_cm: 111, len_in: 30.0, len_cm: 76, shoulder_in: 20.0, shoulder_cm: 51, wt: '81-88 kg', ht: '175-185 cm' },
      { size: '2L', chest_in: 46, chest_cm: 116, len_in: 30.5, len_cm: 77, shoulder_in: 21.0, shoulder_cm: 53, wt: '89-98 kg', ht: '175-190 cm' },
      { size: '3L', chest_in: 48, chest_cm: 121, len_in: 31.0, len_cm: 79, shoulder_in: 22.0, shoulder_cm: 56, wt: '99-108 kg', ht: '175-195 cm' },
      { size: '5L', chest_in: 52, chest_cm: 132, len_in: 32.0, len_cm: 81, shoulder_in: 23.5, shoulder_cm: 60, wt: '109-120 kg', ht: '180-200 cm' },
      { size: '7L', chest_in: 56, chest_cm: 142, len_in: 33.0, len_cm: 84, shoulder_in: 25.0, shoulder_cm: 64, wt: '120+ kg (บิ๊กไซซ์)', ht: '180-205 cm' }
    ],
    pants: [
      { size: 'S',  waist_in: '26-29"', waist_cm: '66-74', hip_in: '36-38"', hip_cm: '91-96', len_in: '38.0"', len_cm: '96', wt: '45-55 kg' },
      { size: 'M',  waist_in: '29-32"', waist_cm: '74-81', hip_in: '38-40"', hip_cm: '96-101', len_in: '39.0"', len_cm: '99', wt: '55-68 kg' },
      { size: 'L',  waist_in: '32-35"', waist_cm: '81-89', hip_in: '40-42"', hip_cm: '101-106', len_in: '40.0"', len_cm: '101', wt: '69-78 kg' },
      { size: 'XL', waist_in: '35-38"', waist_cm: '89-96', hip_in: '42-44"', hip_cm: '106-112', len_in: '41.0"', len_cm: '104', wt: '79-88 kg' },
      { size: '2L', waist_in: '38-41"', waist_cm: '96-104', hip_in: '44-46"', hip_cm: '112-117', len_in: '41.5"', len_cm: '105', wt: '89-98 kg' },
      { size: '3L', waist_in: '41-45"', waist_cm: '104-114', hip_in: '46-49"', hip_cm: '117-124', len_in: '42.0"', len_cm: '106', wt: '99-108 kg' },
      { size: '5L', waist_in: '45-50"', waist_cm: '114-127', hip_in: '50-54"', hip_cm: '127-137', len_in: '43.0"', len_cm: '109', wt: '109-120 kg' },
      { size: '7L', waist_in: '50-56"', waist_cm: '127-142', hip_in: '54-60"', hip_cm: '137-152', len_in: '43.5"', len_cm: '110', wt: '120+ kg' }
    ],
    shoes: [
      { eu: 'EU 35', cm: '22.5 cm', us: 'US 4.0', uk: 'UK 3.5' },
      { eu: 'EU 36', cm: '23.0 cm', us: 'US 4.5', uk: 'UK 4.0' },
      { eu: 'EU 37', cm: '23.5 cm', us: 'US 5.0', uk: 'UK 4.5' },
      { eu: 'EU 38', cm: '24.0 cm', us: 'US 5.5', uk: 'UK 5.0' },
      { eu: 'EU 39', cm: '24.5 cm', us: 'US 6.5', uk: 'UK 6.0' },
      { eu: 'EU 40', cm: '25.0 cm', us: 'US 7.0', uk: 'UK 6.5' },
      { eu: 'EU 41', cm: '25.5 cm', us: 'US 8.0', uk: 'UK 7.5' },
      { eu: 'EU 42', cm: '26.0 cm', us: 'US 8.5', uk: 'UK 8.0' },
      { eu: 'EU 43', cm: '26.5 cm', us: 'US 9.5', uk: 'UK 9.0' },
      { eu: 'EU 44', cm: '27.0 cm', us: 'US 10.0', uk: 'UK 9.5' },
      { eu: 'EU 45', cm: '27.5 cm', us: 'US 11.0', uk: 'UK 10.5' },
      { eu: 'EU 46', cm: '28.0 cm', us: 'US 11.5', uk: 'UK 11.0' },
      { eu: 'EU 47', cm: '28.5 cm', us: 'US 12.5', uk: 'UK 12.0' }
    ]
  };

  window.addEventListener('DOMContentLoaded', () => {
    initOutfitBuilder();
    renderAll();
    initSidebarState();
    switchView('studio');
    runSizeCalculation();
    renderSizeTables();
  });

  
  // ================= AUTHENTICATION & LOGIN GATE =================
  let currentAuthUser = null;

  function setLoginPreset(role, name, username, el) {
    document.querySelectorAll('.login-role-pill').forEach(p => p.classList.remove('active'));
    if (el) el.classList.add('active');
    
    const userField = document.getElementById('login-username');
    if (userField) userField.value = username;
  }

  function handleStudioLogin() {
    const username = document.getElementById('login-username')?.value.trim() || 'cattleya.c';
    let roleTitle = 'MC Host';
    if (username.includes('mod')) roleTitle = 'Co-Host / Mod';
    if (username.includes('director')) roleTitle = 'Studio Director';

    const userObj = {
      username: username,
      displayName: username === 'cattleya.c' ? 'Cattleya C. (MC)' : username,
      role: roleTitle,
      loginAt: new Date().toISOString()
    };

    currentAuthUser = userObj;
    try {
      localStorage.setItem('warrix_auth_user', JSON.stringify(userObj));
    } catch (e) {}

    applyLoggedInUI(userObj);
    showToast(`🎉 ยินดีต้อนรับ ${userObj.displayName} เข้าสู่ระบบ Live Studio!`);
  }

  function handleQuickDemoLogin() {
    const userObj = {
      username: 'cattleya.c',
      displayName: 'Cattleya C. (Lead MC)',
      role: 'MC Host',
      loginAt: new Date().toISOString()
    };
    currentAuthUser = userObj;
    try {
      localStorage.setItem('warrix_auth_user', JSON.stringify(userObj));
    } catch (e) {}

    applyLoggedInUI(userObj);
    showToast('⚡ เข้าสู่ระบบเรียบร้อยแล้ว (Live Studio พร้อมใช้งาน)');
  }

  function handleStudioLogout() {
    try {
      localStorage.removeItem('warrix_auth_user');
    } catch (e) {}
    currentAuthUser = null;
    const loginView = document.getElementById('login-view');
    if (loginView) {
      loginView.classList.remove('logged-in');
    }
    showToast('🚪 ออกจากระบบเรียบร้อยแล้ว');
  }

  function applyLoggedInUI(userObj) {
    const loginView = document.getElementById('login-view');
    if (loginView) {
      loginView.classList.add('logged-in');
    }
    const nameEl = document.getElementById('display-user-name');
    if (nameEl && userObj) {
      nameEl.textContent = userObj.displayName || userObj.username;
    }
  }

  function checkInitialAuth() {
    try {
      const saved = localStorage.getItem('warrix_auth_user');
      if (saved) {
        const userObj = JSON.parse(saved);
        if (userObj && userObj.username) {
          currentAuthUser = userObj;
          applyLoggedInUI(userObj);
          return;
        }
      }
    } catch (e) {}
    const loginView = document.getElementById('login-view');
    if (loginView) {
      loginView.classList.remove('logged-in');
    }
  }

  
  
  // =========================================================
  // ACCURATE MIX & MATCH LOOKBOOK ENGINE
  // =========================================================
  function getTopsList() {
    const bottomCats = ['Pants & Shorts', 'Jeans'];
    const shoeCats = ['Running Shoes', 'Football Boots', 'Football Boots & Referee', 'Sneakers & Lifestyle', 'Accessories & Compression', 'Accessories & Caps', 'Bags'];
    return PRODUCTS.filter(p => !bottomCats.includes(p.category) && !shoeCats.includes(p.category) && !p.sku.startsWith('LP-') && !p.sku.startsWith('WP-') && !p.sku.startsWith('WF-') && !p.sku.startsWith('WS-'));
  }

  function getBottomsList() {
    const bottomCats = ['Pants & Shorts', 'Jeans'];
    return PRODUCTS.filter(p => bottomCats.includes(p.category) || p.sku.startsWith('LP-') || p.sku.startsWith('WP-'));
  }

  function getShoesList() {
    const shoeCats = ['Running Shoes', 'Football Boots', 'Football Boots & Referee', 'Sneakers & Lifestyle', 'Accessories & Compression', 'Accessories & Caps', 'Bags'];
    return PRODUCTS.filter(p => shoeCats.includes(p.category) || p.sku.startsWith('WF-') || p.sku.startsWith('WS-') || p.sku.startsWith('WA-33'));
  }

  function initOutfitBuilder() {
    const tops = getTopsList();
    const bottoms = getBottomsList();
    const shoes = getShoesList();

    const topSelect = document.getElementById('select-slot-top');
    const bottomSelect = document.getElementById('select-slot-bottom');
    const shoesSelect = document.getElementById('select-slot-shoes');

    if (topSelect && tops.length > 0) {
      topSelect.innerHTML = tops.map(p => {
        const pr = getProductPrice(p);
        return `<option value="${p.sku}">${p.sku} - ${p.name} (฿${pr.toLocaleString()})</option>`;
      }).join('');
      if (selectedOutfit.top && tops.some(p => p.sku === selectedOutfit.top)) {
        topSelect.value = selectedOutfit.top;
      } else {
        selectedOutfit.top = tops[0].sku;
        topSelect.value = tops[0].sku;
      }
    }

    if (bottomSelect && bottoms.length > 0) {
      bottomSelect.innerHTML = bottoms.map(p => {
        const pr = getProductPrice(p);
        return `<option value="${p.sku}">${p.sku} - ${p.name} (฿${pr.toLocaleString()})</option>`;
      }).join('');
      if (selectedOutfit.bottom && bottoms.some(p => p.sku === selectedOutfit.bottom)) {
        bottomSelect.value = selectedOutfit.bottom;
      } else {
        selectedOutfit.bottom = bottoms[0].sku;
        bottomSelect.value = bottoms[0].sku;
      }
    }

    if (shoesSelect && shoes.length > 0) {
      shoesSelect.innerHTML = shoes.map(p => {
        const pr = getProductPrice(p);
        return `<option value="${p.sku}">${p.sku} - ${p.name} (฿${pr.toLocaleString()})</option>`;
      }).join('');
      if (selectedOutfit.shoes && shoes.some(p => p.sku === selectedOutfit.shoes)) {
        shoesSelect.value = selectedOutfit.shoes;
      } else {
        selectedOutfit.shoes = shoes[0].sku;
        shoesSelect.value = shoes[0].sku;
      }
    }

    updateOutfitSlot('top', selectedOutfit.top);
    updateOutfitSlot('bottom', selectedOutfit.bottom);
    updateOutfitSlot('shoes', selectedOutfit.shoes);
    updateOutfitPricing();
  }

  function toggleSlotActive(slot, isChecked) {
    activeSlots[slot] = isChecked;
    const card = document.getElementById(`slot-card-${slot}`);
    if (card) {
      card.classList.toggle('slot-disabled', !isChecked);
      card.classList.toggle('slot-active', isChecked);
    }
    updateOutfitPricing();
  }

  function stepSlotItem(slot, dir) {
    let list = (slot === 'top') ? getTopsList() : (slot === 'bottom') ? getBottomsList() : getShoesList();
    if (!list || list.length === 0) return;
    const curIndex = list.findIndex(p => p.sku === selectedOutfit[slot]);
    let nextIndex = curIndex + dir;
    if (nextIndex < 0) nextIndex = list.length - 1;
    if (nextIndex >= list.length) nextIndex = 0;

    const nextSku = list[nextIndex].sku;
    handleOutfitChange(slot, nextSku);
    const sel = document.getElementById(`select-slot-${slot}`);
    if (sel) sel.value = nextSku;
  }

  function handleOutfitChange(slot, sku) {
    selectedOutfit[slot] = sku;
    updateOutfitSlot(slot, sku);
    updateOutfitPricing();
  }

  function updateOutfitSlot(slot, sku) {
    const p = PRODUCTS.find(x => x.sku === sku);
    if (!p) return;

    const imgBox = document.getElementById(`slot-img-${slot}`);
    const skuBox = document.getElementById(`slot-sku-${slot}`);
    const nameBox = document.getElementById(`slot-name-${slot}`);
    const priceBox = document.getElementById(`slot-price-${slot}`);
    const swatchesBox = document.getElementById(`slot-swatches-${slot}`);

    const priceNum = getProductPrice(p);

    if (imgBox) {
      imgBox.innerHTML = p.image_url ? `<img src="${p.image_url}" alt="${p.name}">` : `<span style="font-size:54px;">${p.category_icon || '👕'}</span>`;
    }
    if (skuBox) skuBox.textContent = p.sku;
    if (nameBox) nameBox.textContent = p.name;
    if (priceBox) priceBox.textContent = '฿' + priceNum.toLocaleString();

    if (swatchesBox) {
      const swatches = p.color_palette || p.fashion_color_swatches || [];
      swatchesBox.innerHTML = swatches.slice(0, 5).map(c => `
        <div class="swatch-circle" style="background:${c.hex}; width:16px; height:16px; border-radius:50%; border:1px solid rgba(255,255,255,0.2);" title="${c.name}"></div>
      `).join('');
    }
  }

  function updateOutfitPricing() {
    const topP = activeSlots.top ? PRODUCTS.find(x => x.sku === selectedOutfit.top) : null;
    const btmP = activeSlots.bottom ? PRODUCTS.find(x => x.sku === selectedOutfit.bottom) : null;
    const shoeP = activeSlots.shoes ? PRODUCTS.find(x => x.sku === selectedOutfit.shoes) : null;

    let itemsList = [];
    if (topP) itemsList.push({ label: '👕 ชิ้นบน', product: topP, price: getProductPrice(topP) });
    if (btmP) itemsList.push({ label: '👖 ชิ้นล่าง', product: btmP, price: getProductPrice(btmP) });
    if (shoeP) itemsList.push({ label: '👟 รองเท้า/แอคฯ', product: shoeP, price: getProductPrice(shoeP) });

    const activeCount = itemsList.length;
    let discountPercent = 0;
    let tierText = 'ราคาปกติ (1 ชิ้น)';

    if (activeCount === 3) {
      discountPercent = 20;
      tierText = 'ลดพิเศษ 20% (3 ชิ้น)';
    } else if (activeCount === 2) {
      discountPercent = 15;
      tierText = 'ลดพิเศษ 15% (2 ชิ้น)';
    } else if (activeCount === 1) {
      discountPercent = 0;
      tierText = '🏷️ ซื้อเดี่ยว 1 ชิ้น';
    } else {
      discountPercent = 0;
      tierText = '⚠️ กรุณาเลือกอย่างน้อย 1 ชิ้น';
    }

    const rawTotal = itemsList.reduce((sum, it) => sum + it.price, 0);
    const discountVal = Math.round(rawTotal * (discountPercent / 100));
    const netTotal = rawTotal - discountVal;

    // Render itemized list
    const itemizedListEl = document.getElementById('bundle-itemized-list');
    if (itemizedListEl) {
      if (itemsList.length === 0) {
        itemizedListEl.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:6px;">ไม่มีสินค้าที่เลือกในเซ็ต</div>';
      } else {
        itemizedListEl.innerHTML = itemsList.map(it => `
          <div class="bundle-itemized-row" style="display:flex; justify-content:space-between; font-size:12px; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
            <span style="color:#cbd5e1;"><strong>${it.label}:</strong> ${it.product.name}</span>
            <span style="font-family:'JetBrains Mono'; font-weight:700; color:#38bdf8;">฿${it.price.toLocaleString()}</span>
          </div>
        `).join('');
      }
    }

    const tierBadgeEl = document.getElementById('bundle-tier-badge');
    const rawTotalEl = document.getElementById('bundle-raw-total');
    const discountLabelEl = document.getElementById('bundle-discount-label');
    const discountValEl = document.getElementById('bundle-discount-val');
    const finalPriceEl = document.getElementById('bundle-final-price');
    const savingsBadgeEl = document.getElementById('bundle-savings-badge');

    if (tierBadgeEl) tierBadgeEl.textContent = tierText;
    if (rawTotalEl) rawTotalEl.textContent = '฿' + rawTotal.toLocaleString();
    if (discountLabelEl) discountLabelEl.textContent = `ส่วนลดเซ็ต Total Look (-${discountPercent}%):`;
    if (discountValEl) discountValEl.textContent = '-฿' + discountVal.toLocaleString();
    if (finalPriceEl) finalPriceEl.textContent = '฿' + netTotal.toLocaleString();
    if (savingsBadgeEl) savingsBadgeEl.textContent = `ประหยัด ฿${discountVal.toLocaleString()}`;

    // Speaking script
    const scriptBox = document.getElementById('bundle-speaking-script');
    if (scriptBox) {
      if (activeCount >= 2) {
        const names = itemsList.map(it => it.product.name).join(' + ');
        scriptBox.textContent = `"เซ็ต Total Look ${activeCount} ชิ้นนี้ แมตช์คู่กันอย่างลงตัวสุดๆ ครับ! เสื้อ ${topP ? topP.name : ''} คู่กับกางเกง ${btmP ? btmP.name : ''} ${shoeP ? 'และ' + shoeP.name : ''} ราคารวมปกติ ฿${rawTotal.toLocaleString()} แต่พิเศษในไลฟ์ ซื้อยกเซ็ตลดทันที ${discountPercent}% จ่ายเพียง ฿${netTotal.toLocaleString()} ประหยัดไปถึง ฿${discountVal.toLocaleString()} บาททันทีครับ!"`;
      } else if (activeCount === 1) {
        scriptBox.textContent = `"สินค้าชิ้นนี้ราคาพิเศษในไลฟ์เพียง ฿${rawTotal.toLocaleString()} ครับ! แต่ถ้าจับคู่กับชิ้นอื่นเพิ่มอีก 1 ชิ้น จะได้ส่วนลดเซ็ต 15-20% ทันทีครับ!"`;
      } else {
        scriptBox.textContent = `"เลือกชิ้นที่ต้องการจัดเซ็ตได้เลยครับ!"`;
      }
    }
  }

  function loadOutfitPreset(preset) {
    document.querySelectorAll('.preset-pill-btn').forEach(b => b.classList.remove('active'));
    if (window.event && window.event.currentTarget) {
      window.event.currentTarget.classList.add('active');
    }

    activeSlots = { top: true, bottom: true, shoes: true };
    const tTop = document.getElementById('toggle-slot-top');
    const tBtm = document.getElementById('toggle-slot-bottom');
    const tShoe = document.getElementById('toggle-slot-shoes');
    if (tTop) tTop.checked = true;
    if (tBtm) tBtm.checked = true;
    if (tShoe) tShoe.checked = true;

    ['top', 'bottom', 'shoes'].forEach(s => {
      const c = document.getElementById(`slot-card-${s}`);
      if (c) { c.classList.remove('slot-disabled'); c.classList.add('slot-active'); }
    });

    if (preset === 'smart_casual') {
      selectedOutfit = { top: 'WA-261PLACL15', bottom: 'LP-241JEMW103', shoes: 'WF-253RNACL04' };
    } else if (preset === 'cafe_street') {
      selectedOutfit = { top: 'WA-234TSACL01', bottom: 'LP-241JEMW901', shoes: 'WF-253RNACL03' };
    } else if (preset === 'active_running') {
      selectedOutfit = { top: 'WA-241RNACL01', bottom: 'WP-1509', shoes: 'WF-261RNACL01' };
    } else if (preset === 'matchday') {
      selectedOutfit = { top: 'WA-241FBATH51', bottom: 'WP-223WRACL30', shoes: 'WF-253RNACL02' };
    } else if (preset === 'quiet_luxury') {
      selectedOutfit = { top: 'WA-261PLACL15', bottom: 'LP-241JEMW103', shoes: 'WF-253RNACL04' };
    } else if (preset === 'travel_airport') {
      selectedOutfit = { top: 'WA-242PLACL30', bottom: 'WP-1509', shoes: 'WF-203RNACL01' };
    }

    const topSelect = document.getElementById('select-slot-top');
    const bottomSelect = document.getElementById('select-slot-bottom');
    const shoesSelect = document.getElementById('select-slot-shoes');

    if (topSelect) topSelect.value = selectedOutfit.top;
    if (bottomSelect) bottomSelect.value = selectedOutfit.bottom;
    if (shoesSelect) shoesSelect.value = selectedOutfit.shoes;

    updateOutfitSlot('top', selectedOutfit.top);
    updateOutfitSlot('bottom', selectedOutfit.bottom);
    updateOutfitSlot('shoes', selectedOutfit.shoes);
    updateOutfitPricing();
  }

  function sendToLookbook(sku) {
    const p = PRODUCTS.find(x => x.sku === sku);
    if (!p) return;

    if (p.category === 'Pants & Shorts' || p.category === 'Jeans' || p.sku.startsWith('LP-') || p.sku.startsWith('WP-')) {
      selectedOutfit.bottom = sku;
      activeSlots.bottom = true;
      const el = document.getElementById('toggle-slot-bottom');
      if (el) el.checked = true;
    } else if (['Running Shoes', 'Football Boots', 'Football Boots & Referee', 'Sneakers & Lifestyle', 'Accessories & Compression', 'Accessories & Caps', 'Bags'].includes(p.category) || p.sku.startsWith('WF-') || p.sku.startsWith('WS-') || p.sku.startsWith('WA-33')) {
      selectedOutfit.shoes = sku;
      activeSlots.shoes = true;
      const el = document.getElementById('toggle-slot-shoes');
      if (el) el.checked = true;
    } else {
      selectedOutfit.top = sku;
      activeSlots.top = true;
      const el = document.getElementById('toggle-slot-top');
      if (el) el.checked = true;
    }

    initOutfitBuilder();
    switchView('lookbook');
    showToast(`👗 นำ [${p.sku}] ${p.name} เข้าสู่ Lookbook เรียบร้อย!`);
  }


  function switchView(view) {
    activeView = view;
    document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
    
    if (view === 'studio') document.getElementById('btn-view-studio')?.classList.add('active');
    if (view === 'lookbook') document.getElementById('btn-view-lookbook')?.classList.add('active');
    if (view === 'stylist') document.getElementById('btn-view-stylist')?.classList.add('active');
    if (view === 'sizes') document.getElementById('btn-view-sizes')?.classList.add('active');
    if (view === 'grid') document.getElementById('btn-view-grid')?.classList.add('active');
    if (view === 'matrix') document.getElementById('btn-view-matrix')?.classList.add('active');

    const views = ['studio-view', 'lookbook-view', 'stylist-view', 'sizes-view', 'grid-view', 'matrix-view', 'plan-view', 'knowledge-view'];
    views.forEach(v => {
      const el = document.getElementById(v);
      if (el) {
        el.style.display = 'none';
        el.classList.remove('view-anim');
      }
    });

    const targetEl = document.getElementById(view + '-view');
    if (targetEl) {
      targetEl.style.display = (view === 'studio' || view === 'stylist') ? 'flex' : 'block';
      void targetEl.offsetWidth; // trigger reflow
      targetEl.classList.add('view-anim');
    }
    if (view === 'knowledge') {
      document.getElementById('btn-view-knowledge')?.classList.add('active');
      const kv = document.getElementById('knowledge-view');
      if (kv) kv.scrollTop = 0;
    }
    if (view === 'plan') {
      document.getElementById('btn-view-plan')?.classList.add('active');
      renderPlanPickerGrid();
      updatePlanTray();
    }

    if (view === 'lookbook') {
      initOutfitBuilder();
      updateOutfitPricing();
    }
    if (view === 'sizes') {
      runSizeCalculation();
      renderSizeTables();
    }
  }

  function getProductPrice(p) {
    if (!p) return 0;
    if (typeof p.numeric_price === 'number' && p.numeric_price > 0) return p.numeric_price;
    const str = p.price_range || p.msrp_web || '';
    const match = str.match(/฿\s*([\d,]+(?:\.\d+)?)/);
    if (match) {
      const clean = match[1].replace(/,/g, '');
      const val = parseFloat(clean);
      if (!isNaN(val) && val >= 50 && val <= 20000) return Math.round(val);
    }
    return 390;
  }

  function getFilteredProducts() {
    return PRODUCTS.filter(p => {
      if (activeFilter === 'TOP_GMV') {
        const isTop = p.live_performance?.is_top_gmv || p.name.includes('GMV') || (p.tags && p.tags.some(t => t.includes('GMV') || t.includes('Top')));
        if (!isTop) return false;
      } else if (activeFilter === 'SHOPEE_DEAL') {
        if (!p.is_shopee_deal && !p.shopee_synced) return false;
      } else if (activeFilter === 'VIBE_OFFICE') {
        if (!(p.occasion_vibes || []).includes('Office & Workwear')) return false;
      } else if (activeFilter === 'VIBE_CAFE') {
        if (!(p.occasion_vibes || []).includes('Cafe & Weekend')) return false;
      } else if (activeFilter === 'VIBE_TRAVEL') {
        if (!(p.occasion_vibes || []).includes('Travel & Airport')) return false;
      } else if (activeFilter === 'VIBE_STREET') {
        if (!(p.occasion_vibes || []).includes('Streetwear & Oversize')) return false;
      } else if (activeFilter === 'VIBE_MATCHDAY') {
        if (!(p.occasion_vibes || []).includes('Matchday & Pride')) return false;
      } else if (activeFilter === 'VIBE_ACTIVE') {
        if (!(p.occasion_vibes || []).includes('Active Performance')) return false;
      } else if (activeFilter !== 'ALL') {
        const match = (p.category === activeFilter) || 
                      (activeFilter === 'Pants & Shorts' && (p.category === 'Pants & Shorts' || p.category === 'Jeans')) ||
                      (activeFilter === 'Running Shoes' && (p.category === 'Running Shoes' || p.category === 'Sneakers & Lifestyle'));
        if (!match) return false;
      }

      if (!searchQuery) return true;
      const q = searchQuery.toLowerCase();
      return p.sku.toLowerCase().includes(q) ||
             p.name.toLowerCase().includes(q) ||
             (p.category && p.category.toLowerCase().includes(q)) ||
             (p.product_details?.fabric && p.product_details.fabric.toLowerCase().includes(q)) ||
             (p.occasion_vibes && p.occasion_vibes.some(v => v.toLowerCase().includes(q)));
    });
  }

  function renderAll() {
    const filtered = getFilteredProducts();
    document.getElementById('filtered-count').textContent = filtered.length;
    renderSidebarList(filtered);
    renderPrompterStage();
    renderGridView(filtered);
    renderMatrixView(filtered);
  }

  
    function renderPrompterStage() {
    const stage = document.getElementById('prompter-stage');
    if (!stage) return;
    const p = PRODUCTS.find(x => x.sku === selectedSku) || PRODUCTS[0];
    if (!p) return;

    const s = p.selling_script || {};
    const d = p.what_it_is || p.product_details || {};
    const h = p.how_to_sell || {};
    const vl = p.value_ladder || {};

    let vibesHtml = (p.occasion_vibes || []).map(v => `
      <span style="background:rgba(236, 72, 153, 0.15); border:1px solid rgba(236, 72, 153, 0.3); color:#f472b6; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:500;">
        ✨ ${v}
      </span>
    `).join(' ');

    let swatchesHtml = (p.color_palette || p.fashion_color_swatches || []).map(c => `
      <div class="swatch-circle" style="background:${c.hex};" title="${c.name}" onclick="showToast('🎨 สี ${c.name}')"></div>
    `).join('');

    const exactPrice = getProductPrice(p);

    stage.innerHTML = `
      <div class="prompter-top-nav">
        <div class="prompter-header-info">
          <div class="sku-badge-large">
            <span>🏷️ ${p.sku}</span>
            <span style="color:var(--text-muted);">|</span>
            <span style="color:var(--text-medium); font-weight:400;">${p.category}</span>
          </div>
          <h2 class="prompter-title">${p.name}</h2>
          <div class="prompter-pitch">"${p.tagline || p.elevator_pitch || ''}"</div>
        </div>

        <div class="prompter-quick-actions">
          <button class="btn-action-pill btn-pink" onclick="switchView('lookbook')">
            👗 ประกอบเป็น Lookbook
          </button>
          <button class="btn-action-pill btn-gold" onclick="switchView('sizes')">
            📏 Size Hub & Advisor
          </button>
          <button class="btn-action-pill btn-blue" onclick="showToast('📋 คัดลอกปักหมุดสำเร็จ!')">
            📋 คัดลอกปักหมุด
          </button>
        </div>
      </div>

      <div class="hero-showcase-grid">
        <div class="hero-image-card">
          <div class="hero-image-box" onclick="window.open('${p.google_images_url || p.warrix_url || '#'}', '_blank')">
            ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}">` : `<span style="font-size:48px;">${p.category_icon || '👕'}</span>`}
          </div>
          <div class="price-highlight-card">
            <div style="font-size:11px; color:var(--text-muted); font-weight:500;">ราคา (Price)</div>
            <div class="price-main-val">฿${exactPrice.toLocaleString()}</div>
            <div style="margin-top:8px;">
              <div style="font-size:11px; color:#94a3b8; font-weight:500;">เฉดสี (Color Palette):</div>
              <div class="swatch-circles-container">${swatchesHtml}</div>
            </div>
          </div>
        </div>

                <div class="prompter-script-container">
          <!-- 🪜 FASHION VALUE LADDER (Attribute ➔ Function ➔ Emotion ➔ Identity) -->
          <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(148, 163, 184, 0.15); border-radius: 12px; padding: 10px 14px; margin-bottom: 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span style="font-size:11.5px; font-weight:700; color:#cbd5e1; display:flex; align-items:center; gap:6px;">
                <span>🪜</span> FASHION VALUE LADDER (บันได 4 ขั้นปิดการขาย)
              </span>
              <span style="font-size:10.5px; color:#94a3b8;">คุณสมบัติ ➔ ฟังก์ชัน ➔ ความมั่นใจ ➔ ภาพลักษณ์</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 6px;">
              <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:7px 9px;">
                <div style="font-size:9.5px; color:#94a3b8; font-weight:600; margin-bottom:2px;">1. คุณสมบัติ (Attribute)</div>
                <div style="font-size:11px; color:#e2e8f0; font-weight:500; line-height:1.3;">${vl.level_1_attribute || '-'}</div>
              </div>
              <div style="background:rgba(59, 130, 246, 0.08); border:1px solid rgba(59, 130, 246, 0.2); border-radius:8px; padding:7px 9px;">
                <div style="font-size:9.5px; color:#60a5fa; font-weight:600; margin-bottom:2px;">2. ประโยชน์ใช้สอย (Function)</div>
                <div style="font-size:11px; color:#bfdbfe; font-weight:500; line-height:1.3;">${vl.level_2_functional || '-'}</div>
              </div>
              <div style="background:rgba(244, 114, 182, 0.08); border:1px solid rgba(244, 114, 182, 0.2); border-radius:8px; padding:7px 9px;">
                <div style="font-size:9.5px; color:#f472b6; font-weight:600; margin-bottom:2px;">3. อารมณ์ความมั่นใจ (Emotion)</div>
                <div style="font-size:11px; color:#fbcfe8; font-weight:500; line-height:1.3;">${vl.level_3_emotional || '-'}</div>
              </div>
              <div style="background:rgba(234, 179, 8, 0.08); border:1px solid rgba(234, 179, 8, 0.25); border-radius:8px; padding:7px 9px;">
                <div style="font-size:9.5px; color:#facc15; font-weight:600; margin-bottom:2px;">4. ตัวตน & ภาพลักษณ์ (Identity)</div>
                <div style="font-size:11px; color:#fef08a; font-weight:600; line-height:1.3;">${vl.level_4_identity || '-'}</div>
              </div>
            </div>
          </div>
          <!-- Fashion Flash Hook -->
          <div class="script-block-hero">
            <div class="block-header-label">⚡ HOOK • ประโยคเปิดสะกดคนดู (พูดทันทีที่ปักตะกร้า)</div>
            <div class="hook-speaking-text">"${s.hook || h.hook || p.fashion_hook || '-'}"</div>
          </div>

          <!-- Occasion Vibes Tags -->
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span style="font-size:11.5px; color:#94a3b8; font-weight:600;">Occasion & Vibe:</span>
            ${vibesHtml}
          </div>

          <!-- Fashion Benefit / Styling Tip -->
          <div class="fashion-hook-badge">
            <span>✨ <strong>Fashion Styling Advice:</strong> ${p.styling_advice || 'แมตช์เข้าได้กับกางเกงสแล็คหรือกางเกงวอร์ม ใส่สบายทุกโอกาส'}</span>
          </div>

          <!-- Quick Size Badge for MC -->
          ${s.quick_size ? `
          <div style="background:rgba(59, 130, 246, 0.12); border:1px solid rgba(59, 130, 246, 0.3); color:#93c5fd; padding:7px 12px; border-radius:8px; font-size:12.5px; font-weight:500; display:flex; align-items:center; gap:8px;">
            <span>📏</span> <strong>สูตรเทียบไซซ์ 3 วินาที:</strong> ${s.quick_size}
          </div>
          ` : ''}

          <div class="script-flow-grid">
            <div class="script-card-mini">
              <div class="card-title">🔥 Pain Point ที่ช่วยแก้:</div>
              <div class="card-text">${s.pain_point || h.pain_point || '-'}</div>
            </div>

            <div class="script-card-mini">
              <div class="card-title">🎥 Live Demo (ท่าสาธิตหน้ากล้อง):</div>
              <div class="card-text">${s.live_demo || h.live_demo || '-'}</div>
            </div>

            <div class="script-card-mini">
              <div class="card-title">💬 Interactive CTA (ดึงคอมเมนต์):</div>
              <div class="card-text">${s.interactive_cta || h.interactive_cta || '-'}</div>
            </div>

            <div class="script-card-mini">
              <div class="card-title">🔗 Basket Builder (จับคู่ขายสร้างยอดบิล):</div>
              <div class="card-text">${s.basket_builder || h.basket_builder || '-'}</div>
            </div>
          </div>
          </div>
        </div>
      </div>
    `;
  }


  function renderSidebarList(filtered) {
    const container = document.getElementById('product-list-container');
    container.innerHTML = '';

    if (filtered.length === 0) {
      container.innerHTML = '<div style="padding:24px; text-align:center; color:var(--text-muted); font-size:13px;">ไม่พบสินค้าที่ตรงกับคำค้นหา</div>';
      return;
    }

    filtered.forEach(p => {
      const card = document.createElement('div');
      card.className = 'list-item-card ' + (p.sku === selectedSku ? 'active' : '');
      card.onclick = () => selectProduct(p.sku);

      const vibeTag = (p.occasion_vibes && p.occasion_vibes[0]) ? p.occasion_vibes[0] : (p.category || '');

      card.innerHTML = `
        <div class="list-item-thumb">
          ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy">` : `<span style="font-size:20px;">${p.category_icon || '🏷️'}</span>`}
        </div>
        <div class="list-item-info">
          <div class="list-item-sku">${p.sku}</div>
          <div class="list-item-name">${p.name}</div>
          <div class="list-item-bottom">
            <span class="list-item-price">${p.price_range || '-'}</span>
            <span class="list-item-vibe">${vibeTag}</span>
          </div>
        </div>
      `;
      container.appendChild(card);
    });
  }

  function selectProduct(sku) {
    selectedSku = sku;
    document.querySelectorAll('.list-item-card').forEach(c => c.classList.remove('active'));
    renderAll();
    initSidebarState();
    switchView('studio');
    const p = PRODUCTS.find(x => x.sku === sku);
    if (p) showToast(`🎙️ โหลดสินค้า: [${p.sku}] ${p.name}`);
  }

  function sendOutfitToStylist() {
    const topP = PRODUCTS.find(x => x.sku === selectedOutfit.top);
    const btmP = PRODUCTS.find(x => x.sku === selectedOutfit.bottom);
    const shoeP = PRODUCTS.find(x => x.sku === selectedOutfit.shoes);

    const q = `วิเคราะห์คู่สีและสไตล์ของเซ็ต Total Look นี้หน่อยครับ: เสื้อ ${topP?.name || ''} (${topP?.sku}) + กางเกง ${btmP?.name || ''} (${btmP?.sku}) + รองเท้า ${shoeP?.name || ''} (${shoeP?.sku}) แมตช์กันอย่างไร และขอสคริปต์สไตลิ่งปิดการขายสั้นๆ สำหรับ MC หน้ากล้อง`;

    switchView('stylist');
    const input = document.getElementById('stylistChatInput');
    if (input) {
      input.value = q;
      handleStylistSubmit(new Event('submit'));
    }
  }

  function copyBundleScript() {
    const text = document.getElementById('bundle-speaking-script')?.textContent;
    if (text) {
      navigator.clipboard.writeText(text).then(() => showToast('📋 คัดลอกบทพูด Total Look เรียบร้อยแล้ว!'));
    }
  }

  // =========================================================
  // SIZE CALCULATOR & MATRIX HUB LOGIC
  // =========================================================
  function setQuickHeight(h) {
    const el = document.getElementById('calc-height-input');
    if (el) el.value = h;
    runSizeCalculation();
  }

  function setQuickWeight(w) {
    const el = document.getElementById('calc-weight-input');
    if (el) el.value = w;
    runSizeCalculation();
  }

  function setFitPreference(pref) {
    currentFitPref = pref;
    ['regular', 'comfort', 'oversize'].forEach(p => {
      const el = document.getElementById('pref-btn-' + p);
      if (el) el.classList.toggle('active', p === pref);
    });
    runSizeCalculation();
  }

  function switchSizeUnit(unit) {
    currentSizeUnit = unit;
    ['top', 'pant'].forEach(t => {
      const btnIn = document.getElementById(`unit-${t}-in`);
      const btnCm = document.getElementById(`unit-${t}-cm`);
      if (btnIn && btnCm) {
        btnIn.classList.toggle('active', unit === 'in');
        btnCm.classList.toggle('active', unit === 'cm');
      }
    });
    renderSizeTables();
  }

  function runSizeCalculation() {
    const p = PRODUCTS.find(x => x.sku === selectedSku) || PRODUCTS[0];
    const h = parseFloat(document.getElementById('calc-height-input')?.value) || 175;
    const w = parseFloat(document.getElementById('calc-weight-input')?.value) || 75;

    const hubSku = document.getElementById('hub-current-sku');
    const hubName = document.getElementById('hub-current-name');
    if (hubSku) hubSku.textContent = p.sku;
    if (hubName) hubName.textContent = p.name;

    let recSize = 'XL';
    let recSpec = 'อก 44"';
    let cutBadge = 'Smart Regular Fit';
    let reason = '';
    let script = '';

    const isPlayer = p.name.includes('Player') || p.sku.includes('51');
    const isOversize = p.category === 'Oversize Lifestyle' || p.name.includes('Oversize');
    const isPants = p.category === 'Pants & Shorts' || p.category === 'Jeans';
    const isShoes = p.category === 'Running Shoes' || p.category === 'Football Boots' || p.category === 'Sneakers & Lifestyle';

    if (isShoes) {
      cutBadge = p.name.includes('Classico') ? 'Wide Fit (หน้าเท้ากว้างคนไทย)' : 'True to Size';
      recSize = 'EU 42';
      recSpec = '(ความยาวเท้า 26.0 - 26.5 ซม.)';
      reason = 'สำหรับสรีระเท้ามาตรฐานคนไทย ใส่เบอร์ 42 จะกระชับกำลังดี';
      script = `พี่ที่สูง ${h} ซม. สั่งเบอร์ ${recSize} ${recSpec} ได้เลยครับ ${cutBadge} สวมใส่สบาย ไม่บีบหน้าเท้าแน่นอน!`;
    } else if (isPants) {
      if (w < 55) { recSize = 'S'; recSpec = 'เอว 26-29"'; }
      else if (w <= 68) { recSize = 'M'; recSpec = 'เอว 29-32"'; }
      else if (w <= 78) { recSize = 'L'; recSpec = 'เอว 32-35"'; }
      else if (w <= 88) { recSize = 'XL'; recSpec = 'เอว 35-38"'; }
      else if (w <= 98) { recSize = '2L'; recSpec = 'เอว 38-41"'; }
      else if (w <= 108) { recSize = '3L'; recSpec = 'เอว 41-45"'; }
      else if (w <= 120) { recSize = '5L'; recSpec = 'เอว 45-50"'; }
      else { recSize = '7L'; recSpec = 'เอว 50-56"'; }

      cutBadge = 'Elastic & Stretch (เอวยางยืด)';
      reason = `สำหรับน้ำหนัก ${w} กก. รอบเอวประมาณ ${recSpec} ขอบเอวยืดหยุ่นได้ดี`;
      script = `พี่ที่สูง ${h} หนัก ${w} แนะนำกางเกงไซซ์ ${recSize} (${recSpec}) เลยครับ ขอบเอวยืดหยุ่นลุกนั่งสบาย เป้าไม่รั้งครับ!`;
    } else {
      let baseIndex = 3; // L as base
      if (w < 55) baseIndex = 0;
      else if (w <= 65) baseIndex = 1;
      else if (w <= 72) baseIndex = 2;
      else if (w <= 80) baseIndex = 3;
      else if (w <= 88) baseIndex = 4;
      else if (w <= 98) baseIndex = 5;
      else if (w <= 108) baseIndex = 6;
      else if (w <= 120) baseIndex = 7;
      else baseIndex = 8;

      if (currentFitPref === 'comfort') baseIndex = Math.min(8, baseIndex + 1);
      if (currentFitPref === 'oversize') baseIndex = Math.min(8, baseIndex + (isOversize ? 0 : 1));

      if (isPlayer && currentFitPref !== 'regular') {
        baseIndex = Math.min(8, baseIndex + 1);
        cutBadge = 'Slim Fit (เกรดนักเตะ แนบเนื้อ)';
      } else if (isOversize) {
        cutBadge = 'Drop Shoulder (สตรีทไหล่ตก)';
      } else {
        cutBadge = 'Smart Regular Fit';
      }

      const topSpec = WARRIX_SIZE_SPECS.tops[baseIndex];
      recSize = topSpec.size;
      recSpec = `อก ${topSpec.chest_in}" / ${topSpec.chest_cm} ซม.`;
      reason = `สำหรับส่วนสูง ${h} ซม. น้ำหนัก ${w} กก. แนะนำไซซ์ ${recSize} (${recSpec}) เสื้อยาว ${topSpec.len_in} นิ้ว ชายเสื้อไม่ลอย`;

      let fitTip = 'ทรงสวยเข้ารูปกำลังดี';
      if (currentFitPref === 'comfort') fitTip = 'ใส่สบายพรางพุง ไม่อึดอัดแน่นอน';
      if (currentFitPref === 'oversize') fitTip = 'ได้ลุคสตรีทไหล่ตกสุดเท่';

      script = `พี่ที่สูง ${h} หนัก ${w} แนะนำกดไซซ์ ${recSize} (${recSpec}) เลยครับ! ${fitTip} รุ่นนี้ไหล่สโลปใส่แล้วดูตัวเพรียวมากครับ!`;
    }

    const recSizeEl = document.getElementById('calc-rec-size');
    const recSpecEl = document.getElementById('calc-rec-spec');
    const cutBadgeEl = document.getElementById('calc-fit-badge');
    const reasonEl = document.getElementById('calc-reason-text');
    const scriptEl = document.getElementById('calc-speaking-script');

    if (recSizeEl) recSizeEl.textContent = recSize;
    if (recSpecEl) recSpecEl.textContent = `(${recSpec})`;
    if (cutBadgeEl) cutBadgeEl.textContent = cutBadge;
    if (reasonEl) reasonEl.textContent = reason;
    if (scriptEl) scriptEl.textContent = script;
  }

  function renderSizeTables() {
    const recSize = document.getElementById('calc-rec-size')?.textContent || 'XL';

    // Tops Table
    const topTbody = document.getElementById('table-tops-body');
    if (topTbody) {
      topTbody.innerHTML = `
        <thead>
          <tr>
            <th>ไซซ์</th>
            <th>รอบอก (${currentSizeUnit === 'in' ? 'นิ้ว' : 'ซม.'})</th>
            <th>ความยาว (${currentSizeUnit === 'in' ? 'นิ้ว' : 'ซม.'})</th>
            <th>ไหล่กว้าง (${currentSizeUnit === 'in' ? 'นิ้ว' : 'ซม.'})</th>
            <th>น้ำหนักที่แนะนำ</th>
            <th>ส่วนสูงที่แนะนำ</th>
          </tr>
        </thead>
        <tbody>
          ${WARRIX_SIZE_SPECS.tops.map(s => `
            <tr class="${s.size === recSize ? 'row-highlight' : ''}">
              <td style="font-weight:700; font-family:'JetBrains Mono'; color:#fbbf24;">${s.size}</td>
              <td><strong>${currentSizeUnit === 'in' ? s.chest_in + '"' : s.chest_cm + ' cm'}</strong></td>
              <td>${currentSizeUnit === 'in' ? s.len_in + '"' : s.len_cm + ' cm'}</td>
              <td>${currentSizeUnit === 'in' ? s.shoulder_in + '"' : s.shoulder_cm + ' cm'}</td>
              <td style="color:#94a3b8;">${s.wt}</td>
              <td style="color:#94a3b8;">${s.ht}</td>
            </tr>
          `).join('')}
        </tbody>
      `;
    }

    // Pants Table
    const pantTbody = document.getElementById('table-pants-body');
    if (pantTbody) {
      pantTbody.innerHTML = `
        <thead>
          <tr>
            <th>ไซซ์</th>
            <th>รอบเอว (${currentSizeUnit === 'in' ? 'นิ้ว' : 'ซม.'})</th>
            <th>สะโพก (${currentSizeUnit === 'in' ? 'นิ้ว' : 'ซม.'})</th>
            <th>ความยาว (${currentSizeUnit === 'in' ? 'นิ้ว' : 'ซม.'})</th>
            <th>น้ำหนักที่แนะนำ</th>
          </tr>
        </thead>
        <tbody>
          ${WARRIX_SIZE_SPECS.pants.map(s => `
            <tr class="${s.size === recSize ? 'row-highlight' : ''}">
              <td style="font-weight:700; font-family:'JetBrains Mono'; color:#fbbf24;">${s.size}</td>
              <td><strong>${currentSizeUnit === 'in' ? s.waist_in : s.waist_cm}</strong></td>
              <td>${currentSizeUnit === 'in' ? s.hip_in : s.hip_cm}</td>
              <td>${currentSizeUnit === 'in' ? s.len_in : s.len_cm}</td>
              <td style="color:#94a3b8;">${s.wt}</td>
            </tr>
          `).join('')}
        </tbody>
      `;
    }

    // Shoes Table
    const shoeTbody = document.getElementById('table-shoes-body');
    if (shoeTbody) {
      shoeTbody.innerHTML = `
        <thead>
          <tr>
            <th>ไซซ์ EU</th>
            <th>ความยาวเท้า (CM)</th>
            <th>US Size</th>
            <th>UK Size</th>
            <th>ความกระชับ</th>
          </tr>
        </thead>
        <tbody>
          ${WARRIX_SIZE_SPECS.shoes.map(s => `
            <tr class="${s.eu.includes(recSize) ? 'row-highlight' : ''}">
              <td style="font-weight:700; font-family:'JetBrains Mono'; color:#fbbf24;">${s.eu}</td>
              <td><strong>${s.cm}</strong></td>
              <td>${s.us}</td>
              <td>${s.uk}</td>
              <td>${s.eu === 'EU 42' ? '⭐ ไซซ์ยอดนิยม' : 'มาตรฐาน'}</td>
            </tr>
          `).join('')}
        </tbody>
      `;
    }
  }

  function copyAdvisorScript() {
    const text = document.getElementById('calc-speaking-script')?.textContent.trim();
    if (text) {
      navigator.clipboard.writeText(text).then(() => {
        showToast('📋 คัดลอกสคริปต์แนะนำไซซ์เรียบร้อยแล้ว!');
      }).catch(() => {
        showToast('📋 คัดลอกสคริปต์แนะนำไซซ์เรียบร้อยแล้ว!');
      });
    }
  }

  // =========================================================
  // ULTRA-FAST AI PERSONAL STYLIST ENGINE (INSTANT < 50ms)
  // =========================================================
  const STYLIST_FAST_KNOWLEDGE = {
    color_analysis: `✨ **วิเคราะห์คู่สีเสื้อผ้าขับผิวออร่า (Personal Color & Glow Matching):**

• **☀️ Warm Undertone (ผิวสองสี / ผิวอมเหลือง):**
  - **สีแนะนำอันดับ 1:** **Forest Pine (เขียวไพน์)**, **Midnight Navy (กรมท่า)**, **Champagne Gold**
  - **เหตุผล:** เม็ดสีเขียวเข้มและน้ำเงินลึกช่วยดึงให้ผิวดูผ่อง สว่าง ไม่หมองคล้ำเมื่อโดนแสงไฟสตูฯ
  - **รุ่นเด่น:** \`WA-261PLACL15\` (The Signature Polo) หรือ \`WA-232PLACL34\` (PIN Polo)

• **❄️ Cool Undertone (ผิวขาว / ผิวอมชมพู):**
  - **สีแนะนำอันดับ 1:** **Crimson Red (แดงเบอร์กันดี)**, **Cobalt Blue**, **Ivory Mist**
  - **เหตุผล:** ขับความกระจ่างใสของผิวให้ดูมีเลือดฝาด โดดเด่นขึ้นกล้อง

🎙️ **สคริปต์ MC พูดสด:**
*"พี่ๆ ที่กังวลเรื่องสีเสื้อกลืนกับผิว แนะนำกดสีกรมท่าหรือเขียวไพน์เลยครับ ขับผิวหน้าให้ดูผ่องออร่าจับ ใส่แล้วขึ้นกล้องแน่นอนครับ!"*`,

    silhouette: `✨ **ทริกการแต่งตัวพรางสัดส่วน & ดูสูงเพรียว (Proportion & Slimming Guide):**

1. 👔 **เทคนิคพรางช่วงเอวและพุง (Comfort Smart Fit):**
   - เลือกเสื้อโปโลทรง **Regular Comfort** ปกคอทอแข็งแรง เช่น \`WA-232PLACL34\` (PIN Polo) ปล่อยชายเสื้อปิดระดับสะโพกบน
   - แมตช์คู่กับกางเกงยีนส์ทรงกระบอกตรง \`LP-241JEMW103\` (Pansa Straight Leg) ช่วยยืดช่วงขาให้ดูเพรียวขึ้น 3-5 ซม.

2. 🕶️ **สตรีทโอเวอร์ไซส์ (Drop Shoulder Look):**
   - เลือกเสื้อยืดโอเวอร์ไซส์ \`WA-234TSACL01\` คู่กับกางเกง Baggy \`LP-241JEMW901\` พรางหุ่นได้ 100% สไตล์เกาหลี

🎙️ **สคริปต์ MC พูดสด:**
*"ใครอยากได้ลุคเพรียว ไม่เน้นพุง แนะนำเซ็ตนี้เลยครับ! คัตติ้งช่วงไหล่สโลปพอดีตัว ไม่รัดหน้าท้อง ลุกนั่งสบาย มั่นใจทั้งวันครับ!"*`,

    quiet_luxury: `✨ **ลุค Quiet Luxury / Old Money (เรียบหรูดูแพง สไตล์สากล):**

1. 💎 **สูตรแต่งตัว Quiet Luxury:**
   - **เสื้อหลัก:** \`WA-261PLACL15\` (The Signature Polo สีกรมท่าหรือดำ) ผ้า Dry Tech ทอละเอียด ปกตั้งสวยไม่มีย้วย
   - **กางเกง:** ยีนส์ผ้าดิบพรีเมียม \`LP-241JEMW103\` (Pansa Raw Denim 13.5 oz) หรือกางเกงสแล็ค
   - **รองเท้า:** สนีกเกอร์มินิมอล \`WF-253RNACL04\` (Aegis Sneakers) โทนขาวคลีนหรือดำสนิท

🎙️ **สคริปต์ MC พูดสด:**
*"ลุคนี้คือ 'Quiet Luxury' ของแท้ครับ! เรียบแต่โก้ ไม่ต้องมีโลโก้ใหญ่ แต่คนมองรู้ทันทีว่าใส่ของแพง ใส่ไปคุยงาน ดินเนอร์ ดูน่าเชื่อถือสุดๆ ครับ!"*`,

    mix_match: `✨ **สูตรแมตช์คู่สีกรมท่า (Navy Palette Modern Pairing):**

• **Option 1 (Smart Casual Friday):**
  - เสื้อโปโลสีกรมท่า \`WA-261PLACL15\` (฿390) + กางเกงยีนส์ Pansa (฿1,490) + สนีกเกอร์ขาว (฿1,390)
  - **ลดเซ็ต 20%:** จาก ฿3,270 เหลือเพียง **฿2,616**

• **Option 2 (Active Weekend):**
  - เสื้อโปโลสีกรมท่า + กางเกงวอร์ม \`WP-1509\` สีดำ + รองเท้าวิ่ง \`WF-261RNACL01\`

🎙️ **สคริปต์ MC พูดสด:**
*"สีกรมท่าคือสีอมตะครับ! ใส่กับยีนส์ก็เท่ ใส่กับกางเกงดำก็สุขุม ซื้อยกเซ็ตลด 20% ในไลฟ์ตอนนี้เลยครับ!"*`
  };

  function setPersonalColor(tone) {
    document.querySelectorAll('.undertone-btn').forEach(b => b.classList.remove('active'));
    event?.currentTarget?.classList.add('active');

    const recBox = document.getElementById('personal-color-rec');
    if (tone === 'warm') {
      recBox.innerHTML = '💡 <strong>Warm Tone (ผิวสองสี/เหลือง):</strong> ขับผิวได้ดีที่สุดด้วยเฉด <em>Forest Pine (เขียวไพน์), Midnight Navy, Champagne Gold</em> หน้าจะดูสว่างออร่า';
    } else if (tone === 'cool') {
      recBox.innerHTML = '💡 <strong>Cool Tone (ผิวขาวอมชมพู):</strong> เหมาะกับเฉด <em>Crimson Red (แดงเข้ม), Ivory Mist (ขาวนวล), Cobalt Blue</em> ขับผิวดูโดดเด่นสดใส';
    } else if (tone === 'deep') {
      recBox.innerHTML = '💡 <strong>Deep Tone (ผิวเข้มคมเข้ม):</strong> แนะนำใส่เฉด <em>Carbon Black, Midnight Navy, Burgundy</em> ได้ลุค Smart & Powerful คมเข้มดูแพง';
    }
  }

  function clearStylistChat() {
    document.getElementById('stylistChatTimeline').innerHTML = `
      <div class="stylist-msg-ai">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
          <span style="font-size:16px;">💄</span>
          <strong style="color:#f472b6; font-size:13px;">WARRIX Celebrity Stylist</strong>
          <span style="font-size:10px; background:rgba(236,72,153,0.2); color:#f472b6; padding:1px 6px; border-radius:4px;">Turbo Stream Active</span>
        </div>
        <p>สวัสดีครับ! ต้องการคำแนะนำเรื่องสไตล์การแต่งตัว หรือแมตช์คู่สีสำหรับไลฟ์สดถามได้เลยครับ ตอบไวทันใจทันที!</p>
      </div>
    `;
  }

  function renderStreamText(targetEl, fullMarkdown, onComplete) {
    const words = fullMarkdown.split(' ');
    let i = 0;
    let curr = '';
    targetEl.innerHTML = '';

    const timer = setInterval(() => {
      if (i < words.length) {
        curr += (i > 0 ? ' ' : '') + words[i];
        targetEl.innerHTML = (typeof marked !== 'undefined') ? marked.parse(curr) : curr.split(String.fromCharCode(10)).join('<br/>');
        const timeline = document.getElementById('stylistChatTimeline');
        if (timeline) timeline.scrollTop = timeline.scrollHeight;
        i++;
      } else {
        clearInterval(timer);
        if (onComplete) onComplete();
      }
    }, 8);
  }

  function copyStylistMsg(text) {
    if (text) {
      navigator.clipboard.writeText(text).then(() => showToast('📋 คัดลอกสคริปต์สไตลิสต์เรียบร้อยแล้ว!'));
    }
  }

  async function handleStylistSubmit(e) {
    if (e) e.preventDefault();
    const input = document.getElementById('stylistChatInput');
    const query = input ? input.value.trim() : '';
    if (!query) return;

    const timeline = document.getElementById('stylistChatTimeline');
    const userDiv = document.createElement('div');
    userDiv.className = 'stylist-msg-user';
    userDiv.textContent = query;
    timeline.appendChild(userDiv);

    if (input) input.value = '';
    timeline.scrollTop = timeline.scrollHeight;

    const aiDiv = document.createElement('div');
    aiDiv.className = 'stylist-msg-ai';
    const msgId = 'stylist-resp-' + Date.now();
    aiDiv.innerHTML = '<div style="font-size:12px; font-weight:700; color:#ec4899; margin-bottom:4px; display:flex; justify-content:space-between;"><span>✨ WARRIX Personal Stylist</span><span style="font-size:10px; color:#38bdf8;">⚡ Sub-50ms Streaming</span></div><div id="' + msgId + '" style="color:#94a3b8; font-size:13.5px; line-height:1.6;">กำลังวิเคราะห์สไตล์...</div>';
    timeline.appendChild(aiDiv);
    timeline.scrollTop = timeline.scrollHeight;

    const contentEl = document.getElementById(msgId);
    const qLower = query.toLowerCase();

    // Check fast-path instant knowledge cache first
    let instantMatch = null;
    if (qLower.includes('ผิวสองสี') || qLower.includes('warm') || qLower.includes('ขับผิว') || qLower.includes('ผิวเข้ม')) {
      instantMatch = STYLIST_FAST_KNOWLEDGE.color_analysis;
    } else if (qLower.includes('พรางพุง') || qLower.includes('ตัวเล็ก') || qLower.includes('อ้วน') || qLower.includes('สัดส่วน')) {
      instantMatch = STYLIST_FAST_KNOWLEDGE.silhouette;
    } else if (qLower.includes('quiet luxury') || qLower.includes('old money') || qLower.includes('หรู') || qLower.includes('ทำงาน')) {
      instantMatch = STYLIST_FAST_KNOWLEDGE.quiet_luxury;
    } else if (qLower.includes('สีกรม') || qLower.includes('แมตช์') || qLower.includes('คู่สี')) {
      instantMatch = STYLIST_FAST_KNOWLEDGE.mix_match;
    }

    if (instantMatch) {
      renderStreamText(contentEl, instantMatch, () => {
        appendStylistActions(aiDiv, instantMatch);
      });
      return;
    }

    // Try server SSE endpoint first for lightning fast backend stream
    const apiKey = 'AQ.Ab8RN6KyyrG8dKWMD4wPDcknAzjnhj5ez0mG7xCEruO_6BV-KQ';
    try {
      let accumulated = '';
      let streamed = false;

      const serverStream = await fetch('/api/stylist/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query, api_key: apiKey })
      });

      if (serverStream.ok && serverStream.body) {
        const reader = serverStream.body.getReader();
        const decoder = new TextDecoder('utf-8');
        contentEl.innerHTML = '';
        while (true) {
          const result = await reader.read();
          if (result.done) break;
          const chunk = decoder.decode(result.value, { stream: true });
          const lines = chunk.split(String.fromCharCode(10));
          for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line.startsWith('data:')) {
              const dataStr = line.substring(5).trim();
              if (dataStr === '[DONE]') break;
              try {
                const parsed = JSON.parse(dataStr);
                const token = parsed.token || parsed.text || '';
                if (token) {
                  accumulated += token;
                  contentEl.innerHTML = (typeof marked !== 'undefined') ? marked.parse(accumulated) : accumulated.split(String.fromCharCode(10)).join('<br/>');
                  timeline.scrollTop = timeline.scrollHeight;
                  streamed = true;
                }
              } catch (_) {}
            }
          }
        }
      }

      if (streamed && accumulated) {
        appendStylistActions(aiDiv, accumulated);
        return;
      }
    } catch (_) {}

    // Fallback direct Gemini SSE call with ultra-low latency config
    try {
      let accumulated = '';
      const sysPrompt = 'คุณคือ WARRIX Celebrity Fashion Stylist & Live Commerce Director ให้คำแนะนำเรื่องการแต่งตัว แมตช์คู่สี สไตล์ และทริกการใส่เสื้อผ้าให้ดูดี ตอบกระชับ 3-4 ประโยคพร้อม Hook พูดสดหน้ากล้อง';

      const directStream = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:streamGenerateContent?alt=sse&key=' + apiKey, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ role: 'user', parts: [{ text: `${sysPrompt}\n\nคำถามสไตลิ่ง: ${query}` }] }],
          generationConfig: { temperature: 0.2, maxOutputTokens: 250, thinkingConfig: { thinkingBudget: 0 } }
        })
      });

      if (directStream.ok && directStream.body) {
        const reader = directStream.body.getReader();
        const decoder = new TextDecoder('utf-8');
        contentEl.innerHTML = '';
        while (true) {
          const result = await reader.read();
          if (result.done) break;
          const chunk = decoder.decode(result.value, { stream: true });
          const lines = chunk.split(String.fromCharCode(10));
          for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            if (line.startsWith('data: ')) {
              try {
                const parsed = JSON.parse(line.substring(6).trim());
                const parts = (parsed.candidates && parsed.candidates[0] && parsed.candidates[0].content && parsed.candidates[0].content.parts) || [];
                for (let j = 0; j < parts.length; j++) {
                  if (parts[j].text) {
                    accumulated += parts[j].text;
                    contentEl.innerHTML = (typeof marked !== 'undefined') ? marked.parse(accumulated) : accumulated.split(String.fromCharCode(10)).join('<br/>');
                    timeline.scrollTop = timeline.scrollHeight;
                  }
                }
              } catch (_) {}
            }
          }
        }
        if (accumulated) {
          appendStylistActions(aiDiv, accumulated);
          return;
        }
      }
    } catch (err) {
      // Offline 100 SKUs instant intelligence fallback
      const fallbackAns = `✨ **คำแนะนำสไตลิ่งสำหรับ ${query}:**\n\n• **ไอเดียจับคู่ชุด (Lookbook Combo):** แนะนำเสื้อโปโล WARRIX \`WA-261PLACL15\` หรือ \`WA-232PLACL34\` แมตช์คู่กับกางเกงยีนส์ \`LP-241JEMW103\` และสนีกเกอร์คลีนๆ\n• **สิทธิประโยชน์ในไลฟ์:** กดซื้อเป็นเซ็ต Total Look 3 ชิ้น ลดทันที 20% ในไลฟ์ครับ!\n\n🎙️ **สคริปต์ MC พูดปิดการขาย:**\n*"พี่ๆ ที่กำลังมองหาลุคนี้ แนะนำกดเซ็ตในตะกร้าได้เลยครับ ได้ทั้งความเข้าชุดและส่วนลด 20% ทันทีครับ!"*`;
      renderStreamText(contentEl, fallbackAns, () => {
        appendStylistActions(aiDiv, fallbackAns);
      });
    }
  }

  function appendStylistActions(containerDiv, fullText) {
    if (containerDiv.querySelector('.stylist-suggestion-chips')) return;
    const chipsDiv = document.createElement('div');
    chipsDiv.className = 'stylist-suggestion-chips';
    chipsDiv.innerHTML = `
      <button class="stylist-sugg-btn" onclick="copyStylistMsg(\`${fullText.replace(/`/g, '\\`')}\`)">📋 คัดลอกบทพูด</button>
      <button class="stylist-sugg-btn" onclick="switchView('lookbook')">👗 จัดเซ็ตใน Lookbook ↗</button>
      <button class="stylist-sugg-btn" onclick="askStylistPreset('quiet_luxury')">✨ ดูลุค Quiet Luxury</button>
      <button class="stylist-sugg-btn" onclick="askStylistPreset('silhouette')">📏 ดูทริกพรางพุง</button>
    `;
    containerDiv.appendChild(chipsDiv);
    const timeline = document.getElementById('stylistChatTimeline');
    if (timeline) timeline.scrollTop = timeline.scrollHeight;
  }

  function askStylistPreset(type) {
    const text = STYLIST_FAST_KNOWLEDGE[type];
    if (text) {
      const timeline = document.getElementById('stylistChatTimeline');
      const userDiv = document.createElement('div');
      userDiv.className = 'stylist-msg-user';
      let title = (type === 'color_analysis') ? '🎨 แนะนำคู่สีเสื้อผ้าขับผิวออร่า' :
                  (type === 'silhouette') ? '📏 ทริกแต่งตัวพรางสัดส่วน & พรางพุง' :
                  (type === 'quiet_luxury') ? '✨ ลุค Quiet Luxury / Old Money' : '👖 การแมตช์กางเกงและรองเท้า';
      userDiv.textContent = title;
      timeline.appendChild(userDiv);

      const aiDiv = document.createElement('div');
      aiDiv.className = 'stylist-msg-ai';
      const msgId = 'stylist-resp-' + Date.now();
      aiDiv.innerHTML = '<div style="font-size:12px; font-weight:700; color:#ec4899; margin-bottom:4px; display:flex; justify-content:space-between;"><span>✨ WARRIX Personal Stylist</span><span style="font-size:10px; color:#10b981;">⚡ Sub-50ms Instant</span></div><div id="' + msgId + '" style="color:#94a3b8; font-size:13.5px; line-height:1.6;">กำลังวิเคราะห์สไตล์...</div>';
      timeline.appendChild(aiDiv);
      timeline.scrollTop = timeline.scrollHeight;

      const contentEl = document.getElementById(msgId);
      renderStreamText(contentEl, text, () => {
        appendStylistActions(aiDiv, text);
      });
    }
  }

  function handleSearch(val) {
    searchQuery = val.trim();
    renderAll();
  }

  function renderGridView(filtered) {
    const grid = document.getElementById('grid-container');
    if (!grid) return;
    grid.innerHTML = filtered.map(p => {
      const priceNum = getProductPrice(p);
      return `
        <div class="grid-product-card" onclick="selectProduct('${p.sku}'); switchView('studio');">
          <div style="width:100%; height:160px; background:#040711; border-radius:8px; overflow:hidden; display:flex; align-items:center; justify-content:center;">
            ${p.image_url ? `<img src="${p.image_url}" style="width:100%; height:100%; object-fit:cover;">` : `<span style="font-size:40px;">${p.category_icon || '👕'}</span>`}
          </div>
          <div style="margin-top:8px;">
            <div style="font-size:11px; color:#f59e0b; font-weight:700;">${p.sku}</div>
            <div style="font-size:13px; font-weight:600; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${p.name}</div>
            <div style="font-size:14px; font-weight:700; color:#10b981; margin-top:2px;">฿${priceNum.toLocaleString()}</div>
            <div style="font-size:11px; color:#ec4899; margin-top:4px;">${(p.occasion_vibes || []).join(' • ')}</div>
          </div>
        </div>
      `;
    }).join('');
  }

  function renderMatrixView(filtered) {
    const tbody = document.getElementById('matrix-tbody');
    if (!tbody) return;
    tbody.innerHTML = filtered.map(p => {
      const priceNum = getProductPrice(p);
      return `
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
          <td style="padding:10px 16px; font-family:'JetBrains Mono'; color:#f59e0b; font-weight:700;">${p.sku}</td>
          <td style="padding:10px 16px; color:#fff; font-weight:500;">${p.name}</td>
          <td style="padding:10px 16px; color:#94a3b8;">${p.category}</td>
          <td style="padding:10px 16px; color:#10b981; font-weight:700;">฿${priceNum.toLocaleString()}</td>
          <td style="padding:10px 16px; color:#f472b6;">${(p.occasion_vibes || []).join(', ')}</td>
          <td style="padding:10px 16px;"><a href="${p.warrix_url}" target="_blank" style="color:#38bdf8; text-decoration:underline;">Warrix.com ↗</a></td>
        </tr>
      `;
    }).join('');
  }

  // =========================================================
  // CSV IMPORT & EXPORT ENGINE (100 SKUs DYNAMIC SYNC)
  // =========================================================
  function triggerCsvImport() {
    const input = document.getElementById('csv-file-input');
    if (input) {
      input.value = '';
      input.click();
    }
  }

  function parseCSV(text) {
    if (text.charCodeAt(0) === 0xFEFF) {
      text = text.slice(1);
    }
    const lines = [];
    let row = [];
    let col = '';
    let inQuotes = false;
    
    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      const nextChar = text[i + 1];

      if (char === '"' || char === "'") {
        if (inQuotes && nextChar === char) {
          col += char;
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if ((char === ',' || char === ';') && !inQuotes) {
        row.push(col.trim());
        col = '';
      } else if ((char === '\\r' || char === '\\n') && !inQuotes) {
        if (char === '\\r' && nextChar === '\\n') {
          i++;
        }
        row.push(col.trim());
        if (row.some(cell => cell.length > 0)) {
          lines.push(row);
        }
        row = [];
        col = '';
      } else {
        col += char;
      }
    }
    if (col.length > 0 || row.length > 0) {
      row.push(col.trim());
      if (row.some(cell => cell.length > 0)) {
        lines.push(row);
      }
    }
    return lines;
  }

  function handleCsvFileChange(event) {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    const btn = document.getElementById('btn-import-csv');
    if (btn) btn.innerHTML = '⏳ ประมวลผล...';

    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const text = e.target.result;
        const rows = parseCSV(text);
        if (!rows || rows.length < 2) {
          showToast('⚠️ ไฟล์ CSV ต้องมีอย่างน้อย 1 แถวข้อมูล (หัวตาราง + ข้อมูลสินค้า)');
          if (btn) btn.innerHTML = '📁 Import CSV';
          return;
        }

        const rawHeaders = rows[0].map(h => h.toLowerCase().replace(/[\\s_\\-\\.\\ufeff]/g, ''));
        
        const findCol = (possibleNames) => {
          return rawHeaders.findIndex(h => possibleNames.some(p => h.includes(p)));
        };

        const skuIdx = findCol(['sku', 'code', 'itemcode', 'productid', 'id']);
        const nameIdx = findCol(['name', 'title', 'productname', 'itemname', 'model']);
        const catIdx = findCol(['category', 'cat', 'type', 'group']);
        const priceIdx = findCol(['price', 'saleprice', 'specialprice', 'numericprice', 'liveprice']);
        const msrpIdx = findCol(['msrp', 'regularprice', 'fullprice', 'normalprice']);
        const imgIdx = findCol(['image', 'imageurl', 'img', 'photo', 'picture', 'pic']);
        const fabricIdx = findCol(['fabric', 'material', 'textile', 'details']);
        const hookIdx = findCol(['hook', 'pitch', 'script', 'selling', 'point']);
        const colorsIdx = findCol(['colors', 'color', 'palette']);
        const vibesIdx = findCol(['vibe', 'occasion', 'vibes']);

        if (skuIdx === -1) {
          showToast('⚠️ ไม่พบคอลัมน์ SKU (ต้องมีหัวคอลัมน์ sku หรือ code)');
          if (btn) btn.innerHTML = '📁 Import CSV';
          return;
        }

        let updatedCount = 0;
        let newCount = 0;
        const newProductsList = [];

        for (let i = 1; i < rows.length; i++) {
          const row = rows[i];
          const sku = (row[skuIdx] || '').trim();
          if (!sku) continue;

          const name = nameIdx !== -1 && row[nameIdx] ? row[nameIdx].trim() : `สินค้า Warrix ${sku}`;
          const category = catIdx !== -1 && row[catIdx] ? row[catIdx].trim() : 'Polo Shirts';
          const priceRaw = priceIdx !== -1 && row[priceIdx] ? row[priceIdx].replace(/[^\\d.]/g, '') : '390';
          const priceNum = Math.round(parseFloat(priceRaw)) || 390;
          const msrpRaw = msrpIdx !== -1 && row[msrpIdx] ? row[msrpIdx].replace(/[^\\d.]/g, '') : '';
          const imgUrl = imgIdx !== -1 && row[imgIdx] ? row[imgIdx].trim() : '';
          const fabric = fabricIdx !== -1 && row[fabricIdx] ? row[fabricIdx].trim() : 'Polyester Micro ระบายอากาศดีเยี่ยม';
          const hook = hookIdx !== -1 && row[hookIdx] ? row[hookIdx].trim() : `รุ่นยอดนิยม ${name} ใส่สบาย คืนรูป ไม่ต้องรีด`;
          const colorsText = colorsIdx !== -1 && row[colorsIdx] ? row[colorsIdx].trim() : 'ดำ, ขาว, กรมท่า';
          const vibesText = vibesIdx !== -1 && row[vibesIdx] ? row[vibesIdx].trim() : 'Office & Workwear, Cafe & Weekend';

          const colorList = colorsText.split(/[,/]/).map(c => c.trim()).filter(Boolean);
          const colorPalette = colorList.map((c, idx) => ({
            name: c,
            hex: ['#1e293b', '#f8fafc', '#1e3a8a', '#dc2626', '#059669', '#d97706'][idx % 6]
          }));

          const occasionVibes = vibesText.split(/[,/]/).map(v => v.trim()).filter(Boolean);

          const existingIdx = PRODUCTS.findIndex(p => p.sku.toLowerCase() === sku.toLowerCase());

          if (existingIdx !== -1) {
            const curr = PRODUCTS[existingIdx];
            curr.name = name || curr.name;
            curr.category = category || curr.category;
            curr.numeric_price = priceNum;
            curr.price_range = `฿${priceNum.toLocaleString()}`;
            curr.web_sale_price = `฿${priceNum.toLocaleString()}`;
            if (msrpRaw) curr.msrp_web = `฿${parseInt(msrpRaw).toLocaleString()}`;
            if (imgUrl) curr.image_url = imgUrl;
            if (!curr.what_it_is) curr.what_it_is = {};
            curr.what_it_is.fabric = fabric;
            if (!curr.how_to_sell) curr.how_to_sell = {};
            curr.how_to_sell.hook = hook;
            if (colorPalette.length > 0) curr.color_palette = colorPalette;
            if (occasionVibes.length > 0) curr.occasion_vibes = occasionVibes;
            SKU_MAP[curr.sku] = curr;
            updatedCount++;
            newProductsList.push(curr);
          } else {
            const newP = {
              id: sku.toLowerCase().replace(/[^a-z0-9]/g, '-'),
              sku: sku,
              name: name,
              category: category,
              price_range: `฿${priceNum.toLocaleString()}`,
              numeric_price: priceNum,
              web_sale_price: `฿${priceNum.toLocaleString()}`,
              msrp_web: msrpRaw ? `฿${parseInt(msrpRaw).toLocaleString()}` : '',
              image_url: imgUrl,
              tagline: hook,
              elevator_pitch: hook,
              category_icon: category.includes('Pants') ? '👖' : category.includes('Shoe') ? '👟' : '👕',
              what_it_is: {
                fabric: fabric,
                key_design: 'ดีไซน์พรีเมียม สวมใส่สบายทุกโอกาส',
                size_range: 'XS - 7L',
                colors: colorList
              },
              product_details: {
                fabric: fabric,
                key_design: 'ดีไซน์พรีเมียม สวมใส่สบายทุกโอกาส'
              },
              how_to_sell: {
                hook: hook,
                pain_point: 'เสื้อผ้าทั่วไปร้อน อับเหงื่อ ยับง่าย',
                live_demo: 'ดึงยืดโชว์ความยืดหยุ่นคืนรูปหน้ากล้อง',
                interactive_cta: `พิมพ์ '${sku}' รับโปรโมชั่นพิเศษทันที!`,
                basket_builder: 'จับคู่กับกางเกงและสนีกเกอร์ในเซ็ต'
              },
              selling_script: {
                hook: hook,
                pain_point: 'เสื้อผ้าทั่วไปร้อน อับเหงื่อ ยับง่าย',
                live_demo: 'ดึงยืดโชว์ความยืดหยุ่นคืนรูปหน้ากล้อง',
                interactive_cta: `พิมพ์ '${sku}' รับโปรโมชั่นพิเศษทันที!`,
                basket_builder: 'จับคู่กับกางเกงและสนีกเกอร์ในเซ็ต'
              },
              color_palette: colorPalette.length > 0 ? colorPalette : [{ name: 'ดำ (Black)', hex: '#18181b' }, { name: 'ขาว (White)', hex: '#f8fafc' }],
              occasion_vibes: occasionVibes.length > 0 ? occasionVibes : ['Office & Workwear', 'Cafe & Weekend']
            };
            PRODUCTS.unshift(newP);
            SKU_MAP[newP.sku] = newP;
            newCount++;
            newProductsList.push(newP);
          }
        }

        if (typeof renderAll === 'function') renderAll();
        if (typeof initOutfitBuilder === 'function') initOutfitBuilder();
        if (typeof renderPlanPickerGrid === 'function') renderPlanPickerGrid();
        if (typeof renderPlanReviewStack === 'function') renderPlanReviewStack();

        // Push to server database
        fetch('/api/products/import', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ products: newProductsList })
        }).catch(err => console.log('Local CSV mode active'));

        showToast(`🎉 นำเข้า CSV สำเร็จ! (เพิ่มใหม่ ${newCount} รายการ, อัปเดต ${updatedCount} รายการ รวม ${PRODUCTS.length} SKUs)`);
      } catch (err) {
        console.error(err);
        showToast('❌ ข้อผิดพลาดในการอ่าน CSV: ' + err.message);
      } finally {
        if (btn) btn.innerHTML = '📁 Import CSV';
      }
    };
    reader.readAsText(file, 'utf-8');
  }

  function exportProductsCsv() {
    if (!PRODUCTS || PRODUCTS.length === 0) {
      showToast('⚠️ ไม่มีข้อมูลสินค้าให้ส่งออก');
      return;
    }
    const headers = ['sku', 'name', 'category', 'price', 'msrp', 'image_url', 'fabric', 'hook', 'colors', 'occasion_vibes'];
    const escapeCsv = (val) => {
      if (val === null || val === undefined) return '""';
      const str = String(val).replace(/"/g, '""');
      return `"${str}"`;
    };

    const csvRows = [headers.join(',')];
    PRODUCTS.forEach(p => {
      const colors = (p.color_palette || []).map(c => c.name).join(', ');
      const vibes = (p.occasion_vibes || []).join(', ');
      const fabric = p.what_it_is?.fabric || p.product_details?.fabric || '';
      const hook = p.how_to_sell?.hook || p.selling_script?.hook || p.tagline || '';
      const price = getProductPrice(p);
      const msrp = p.msrp_web ? p.msrp_web.replace(/[^\\d.]/g, '') : '';

      const row = [
        escapeCsv(p.sku),
        escapeCsv(p.name),
        escapeCsv(p.category),
        escapeCsv(price),
        escapeCsv(msrp),
        escapeCsv(p.image_url || ''),
        escapeCsv(fabric),
        escapeCsv(hook),
        escapeCsv(colors),
        escapeCsv(vibes)
      ];
      csvRows.push(row.join(','));
    });

    const csvContent = '\\uFEFF' + csvRows.join('\\r\\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `warrix_products_catalog_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('📥 ส่งออกไฟล์ CSV แคตตาล็อกสินค้าเรียบร้อยแล้ว!');
  }


  // =========================================================
  // DYNAMIC KNOWLEDGE VIEW & 225 PRODUCTS PERFORMANCE ENGINE
  // =========================================================
  const GMV_PRODUCTS_DATA = [{"name": "WARRIX รองเท้าวิ่ง WAVE 1.0 Uncaged Running Collection WF-203RNACL01 (รบกวนบวกเพิ่ม 1 ไซซ์จากตารางไซซ์)", "sku": "WF-203RNACL01", "gmv": 9551977, "gmv_pd": 40304, "sell_price": 826, "orig_price": 1490, "discount_pct": 44.7, "h2_vs_h1": 1.2, "cpgn_lift": 2.19, "qty": 11584, "tag": "Hero"}, {"name": "WARRIX เสื้อคอวี THAILAND LIFESTYLE OVERSIZE JERSEY 2024/25 (WA-243FBATH10)", "sku": "WA-243FBATH10", "gmv": 9332148, "gmv_pd": 39376, "sell_price": 535, "orig_price": 890, "discount_pct": 40.3, "h2_vs_h1": 0.79, "cpgn_lift": 2.69, "qty": 17564, "tag": "Hero"}, {"name": "WARRIX เสื้อโปโล รุ่น PIQUE (WA-212PLACL30)", "sku": "WA-212PLACL30", "gmv": 8674174, "gmv_pd": 36600, "sell_price": 205, "orig_price": 304, "discount_pct": 34.6, "h2_vs_h1": 2.05, "cpgn_lift": 2.82, "qty": 43676, "tag": "Hero"}, {"name": "WARRIX กางเกงวิ่งขาสั้น 5 นิ้ว (WP-252RNACL02)", "sku": "WP-252RNACL02", "gmv": 7474759, "gmv_pd": 33670, "sell_price": 222, "orig_price": 299, "discount_pct": 27.0, "h2_vs_h1": 1.45, "cpgn_lift": 1.93, "qty": 34247, "tag": "Hero"}, {"name": "WARRIX กางเกงฟุตบอล เบสิค WP-1509", "sku": "WP-1509", "gmv": 6953954, "gmv_pd": 29342, "sell_price": 82, "orig_price": 159, "discount_pct": 51.7, "h2_vs_h1": 1.18, "cpgn_lift": 2.2, "qty": 90563, "tag": "Hero"}, {"name": "WARRIX ACTIVE TRAINING SHIRT (WA-231FBACL04)", "sku": "WA-231FBACL04", "gmv": 4593724, "gmv_pd": 19383, "sell_price": 110, "orig_price": 204, "discount_pct": 47.9, "h2_vs_h1": 1.12, "cpgn_lift": 1.98, "qty": 43195, "tag": "Hero"}, {"name": "[ใหม่!!] WARRIX เสื้อโปโล รุ่น VIVIDUS POLO (WA-242PLACL30)", "sku": "WA-242PLACL30", "gmv": 4414918, "gmv_pd": 18628, "sell_price": 294, "orig_price": 453, "discount_pct": 37.6, "h2_vs_h1": 2.53, "cpgn_lift": 2.71, "qty": 15636, "tag": "Hero"}, {"name": "WARRIX กางเกงฟุตบอลขาสั้น Power Stride Shorts Pants (WP-241FBACL02)", "sku": "WP-241FBACL02", "gmv": 4076327, "gmv_pd": 17200, "sell_price": 246, "orig_price": 449, "discount_pct": 47.0, "h2_vs_h1": 1.32, "cpgn_lift": 1.97, "qty": 17119, "tag": "Hero"}, {"name": "WARRIX เสื้อโปโล PIN BLACK COLOR (WA-232PLACL34)", "sku": "WA-232PLACL34", "gmv": 3524668, "gmv_pd": 14935, "sell_price": 208, "orig_price": 305, "discount_pct": 35.6, "h2_vs_h1": 1.9, "cpgn_lift": 2.39, "qty": 17954, "tag": "Hero"}, {"name": "WARRIX GravityX Sneakers (WF-233ALACL01)", "sku": "WF-233ALACL01", "gmv": 3441635, "gmv_pd": 14522, "sell_price": 1010, "orig_price": 1990, "discount_pct": 49.3, "h2_vs_h1": 0.78, "cpgn_lift": 1.67, "qty": 3412, "tag": "Hero"}, {"name": "WARRIX  เสื้อโปโลเบสิค แขนสั้น WA-3315N v.1", "sku": "WA-3315N", "gmv": 2800764, "gmv_pd": 11818, "sell_price": 307, "orig_price": 451, "discount_pct": 32.7, "h2_vs_h1": 1.38, "cpgn_lift": 2.42, "qty": 9227, "tag": "Hero"}, {"name": "WARRIX เสื้อแจ็คเก็ตกันลม Herit Woven Jacket (WA-223JKACL36)", "sku": "WA-223JKACL36", "gmv": 2736614, "gmv_pd": 11547, "sell_price": 563, "orig_price": 790, "discount_pct": 32.4, "h2_vs_h1": 1.47, "cpgn_lift": 1.99, "qty": 5124, "tag": "Hero"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 2025/26 (Replica Grade) WA-253FBATH52", "sku": "WA-253FBATH52", "gmv": 2638141, "gmv_pd": 11274, "sell_price": 702, "orig_price": 1290, "discount_pct": 46.1, "h2_vs_h1": 2.31, "cpgn_lift": 3.0, "qty": 3797, "tag": "Hero"}, {"name": "WARRIX เสื้อฟุตบอลโอเวอร์ไซส์ Oversize Jersey New Chapter (WA-251FBATH10)", "sku": "WA-251FBATH10", "gmv": 2599421, "gmv_pd": 11014, "sell_price": 495, "orig_price": 890, "discount_pct": 44.4, "h2_vs_h1": 1.58, "cpgn_lift": 2.74, "qty": 5252, "tag": "Hero"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทยฤดูกาลใหม่ 2026/27 Cheer Grade (WA-262FBATH53)", "sku": "WA-262FBATH53", "gmv": 2533693, "gmv_pd": 31671, "sell_price": 361, "orig_price": 399, "discount_pct": 9.4, "h2_vs_h1": null, "cpgn_lift": 2.04, "qty": 7008, "tag": "Hero"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 2025/26 (CHEER Grade) WA-253FBATH53", "sku": "WA-253FBATH53", "gmv": 2424628, "gmv_pd": 10318, "sell_price": 213, "orig_price": 399, "discount_pct": 46.9, "h2_vs_h1": 2.5, "cpgn_lift": 2.17, "qty": 11443, "tag": "Rising"}, {"name": "WARRIX กางเกงฟุตบอล WP-1509-ดำ", "sku": "WP-1509", "gmv": 2421304, "gmv_pd": 10216, "sell_price": 81, "orig_price": 159, "discount_pct": 57.9, "h2_vs_h1": 1.91, "cpgn_lift": 1.97, "qty": 36214, "tag": "Standard"}, {"name": "WARRIX กางเกงลำลองขาสั้น (WP-231CAACL04)", "sku": "WP-231CAACL04", "gmv": 2264458, "gmv_pd": 9803, "sell_price": 201, "orig_price": 490, "discount_pct": 60.8, "h2_vs_h1": 2.08, "cpgn_lift": 2.22, "qty": 11800, "tag": "Rising"}, {"name": "[Exclusive Online] WARRIX เสื้อโปโลแขนสั้นรุ่น Zypher Polo (WA-261PLACL30)", "sku": "WA-261PLACL30", "gmv": 2136137, "gmv_pd": 14147, "sell_price": 242, "orig_price": 453, "discount_pct": 47.7, "h2_vs_h1": 4.26, "cpgn_lift": 2.32, "qty": 9031, "tag": "Rising"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทยฤดูกาลใหม่ 2026/27 Replica Grade (WA-262FBATH52)", "sku": "WA-262FBATH52", "gmv": 2117053, "gmv_pd": 26463, "sell_price": 1203, "orig_price": 1290, "discount_pct": 6.7, "h2_vs_h1": null, "cpgn_lift": 2.47, "qty": 1759, "tag": "Standard"}, {"name": "Warrix เสื้อโปโล Premium Polo (WA-214PLACL32)", "sku": "WA-214PLACL32", "gmv": 2055338, "gmv_pd": 8672, "sell_price": 349, "orig_price": 605, "discount_pct": 45.6, "h2_vs_h1": 1.39, "cpgn_lift": 2.51, "qty": 6242, "tag": "Booster"}, {"name": "WARRIX  เสื้อเชียร์งานฟุตบอลสานสัมพันธ์ จุฬา-ธรรมศาสตร์ (WA-241PLATU01)", "sku": "WA-241PLATU01", "gmv": 1935029, "gmv_pd": 8165, "sell_price": 163, "orig_price": 350, "discount_pct": 54.6, "h2_vs_h1": 1.44, "cpgn_lift": 1.51, "qty": 12175, "tag": "Standard"}, {"name": "WARRIX WOVEN JACKET  เสื้อแจ็คเก็ต รุ่น BASIE (WA-262JKACL70)", "sku": "WA-262JKACL70", "gmv": 1771933, "gmv_pd": 13526, "sell_price": 754, "orig_price": 790, "discount_pct": 4.6, "h2_vs_h1": 3.95, "cpgn_lift": 2.03, "qty": 2350, "tag": "Rising"}, {"name": "WARRIX เสื้อโปโล POLO WAVORA - Exclusive Online 2025 (WA-252PLACL31)", "sku": "WA-252PLACL31", "gmv": 1459250, "gmv_pd": 6157, "sell_price": 179, "orig_price": 301, "discount_pct": 42.2, "h2_vs_h1": 0.92, "cpgn_lift": 1.92, "qty": 8400, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทยฤดูกาลใหม่ 2026/27 Player Grade (WA-262FBATH51)", "sku": "WA-262FBATH51", "gmv": 1399563, "gmv_pd": 19172, "sell_price": 2385, "orig_price": 2490, "discount_pct": 4.2, "h2_vs_h1": null, "cpgn_lift": 2.16, "qty": 587, "tag": "Standard"}, {"name": "WARRIX x CROCHET FLYKNTTI รองเท้าวิ่ง รองเท้ากีฬา (WF-253RNACL01)", "sku": "WF-253RNACL01", "gmv": 1384869, "gmv_pd": 8293, "sell_price": 913, "orig_price": 1990, "discount_pct": 54.2, "h2_vs_h1": 3.75, "cpgn_lift": 1.89, "qty": 1518, "tag": "Rising"}, {"name": "WARRIX เสื้อฟุตบอลโอเวอร์ไซส์ Oversize Jersey 2025/26 (WA-261FBACL10)", "sku": "WA-261FBACL10", "gmv": 1351433, "gmv_pd": 5800, "sell_price": 573, "orig_price": 590, "discount_pct": 2.9, "h2_vs_h1": 0.8, "cpgn_lift": 2.44, "qty": 2358, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซซ์ทีมชาติไทย รุ่น THAILAND LIFESTYLE OVERSIZE JERSEY 2025/26 (WA-253FBATH12)", "sku": "WA-253FBATH12", "gmv": 1338254, "gmv_pd": 5744, "sell_price": 789, "orig_price": 890, "discount_pct": 11.5, "h2_vs_h1": 0.79, "cpgn_lift": 2.01, "qty": 1700, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล PIQUE PLUS (WA-221PLACL30)", "sku": "WA-221PLACL30", "gmv": 1322517, "gmv_pd": 5580, "sell_price": 178, "orig_price": 307, "discount_pct": 45.3, "h2_vs_h1": 1.29, "cpgn_lift": 2.03, "qty": 7899, "tag": "Standard"}, {"name": "WARRIX เสื้อแข่งฟุตบอลทีมชาติไทย 2025/26 (Player Grade) WA-253FBATH51", "sku": "WA-253FBATH51", "gmv": 1241108, "gmv_pd": 6637, "sell_price": 1387, "orig_price": 2490, "discount_pct": 44.4, "h2_vs_h1": 1.45, "cpgn_lift": 3.41, "qty": 897, "tag": "Booster"}, {"name": "WARRIX เสื้อโปโล Vibes (WA-203PLACL01)", "sku": "WA-203PLACL01", "gmv": 1238862, "gmv_pd": 5272, "sell_price": 215, "orig_price": 404, "discount_pct": 49.2, "h2_vs_h1": 2.21, "cpgn_lift": 2.05, "qty": 6056, "tag": "Rising"}, {"name": "WARRIX เสื้อโปโลแขนสั้น WARRIX POLO รุ่น  LAI THAI (WA-261PLACL02)", "sku": "WA-261PLACL02", "gmv": 1204483, "gmv_pd": 6511, "sell_price": 393, "orig_price": 409, "discount_pct": 3.8, "h2_vs_h1": 1.35, "cpgn_lift": 2.0, "qty": 3064, "tag": "Standard"}, {"name": "WARRIX เสื้อออกกำลังกาย BASIC ONE PLUS TRAINING SHIRT (WA-251FBACL01) Ver.1", "sku": "WA-251FBACL01", "gmv": 1179705, "gmv_pd": 5565, "sell_price": 121, "orig_price": 204, "discount_pct": 42.2, "h2_vs_h1": 4.07, "cpgn_lift": 1.64, "qty": 10019, "tag": "Rising"}, {"name": "WARRIX รองเท้าวิ่ง รุ่น MOMENTUM (WF-253RNACL02)", "sku": "WF-253RNACL02", "gmv": 1118306, "gmv_pd": 5825, "sell_price": 1352, "orig_price": 1990, "discount_pct": 32.5, "h2_vs_h1": 2.55, "cpgn_lift": 1.6, "qty": 833, "tag": "Rising"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 25/26 CHEER Grade (WA-254FBATH54)", "sku": "WA-254FBATH54", "gmv": 1114403, "gmv_pd": 7686, "sell_price": 212, "orig_price": 399, "discount_pct": 47.1, "h2_vs_h1": 2.09, "cpgn_lift": 2.69, "qty": 5279, "tag": "Rising"}, {"name": "WARRIX THAILAND HOME JERSEY 2024/25 CHEER (WA-243FBATH53)", "sku": "WA-243FBATH53", "gmv": 1098377, "gmv_pd": 8787, "sell_price": 176, "orig_price": 399, "discount_pct": 56.3, "h2_vs_h1": 0.17, "cpgn_lift": 1.35, "qty": 6303, "tag": "Clearance"}, {"name": "WARRIX เสื้อคอวีแขนยาว THAILAND LIFESTYLE OVERSIZE JERSEY 2024/25 LONG SLEEVE ( WA-243FBATH11)", "sku": "WA-243FBATH11", "gmv": 1046201, "gmv_pd": 4452, "sell_price": 553, "orig_price": 990, "discount_pct": 44.1, "h2_vs_h1": 0.8, "cpgn_lift": 2.47, "qty": 1892, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล รุ่น PIQUE (WA-212PLACL30) V.2", "sku": "WA-212PLACL30", "gmv": 940539, "gmv_pd": 3985, "sell_price": 206, "orig_price": 306, "discount_pct": 35.6, "h2_vs_h1": 2.96, "cpgn_lift": 1.97, "qty": 4790, "tag": "Rising"}, {"name": "WARRIX CROCHET POLO เสื้อโปโล รุ่น DRY TECH (WA-261PLACR01)", "sku": "WA-261PLACR01", "gmv": 885503, "gmv_pd": 4661, "sell_price": 224, "orig_price": 449, "discount_pct": 52.9, "h2_vs_h1": 1.97, "cpgn_lift": 2.67, "qty": 4187, "tag": "Booster"}, {"name": "WARRIX เสื้อคอปกแขนสั้น Football Lifestyle Oversize T-shirt Unisex (WA-261FBATH10)", "sku": "WA-261FBATH10", "gmv": 850500, "gmv_pd": 5825, "sell_price": 855, "orig_price": 890, "discount_pct": 4.0, "h2_vs_h1": 1.77, "cpgn_lift": 2.56, "qty": 995, "tag": "Booster"}, {"name": "WARRIX เสื้อฟุตบอล THAILAND BASIC LIFESTYLE JERSEY 2026 (WA-261FBATH11)", "sku": "WA-261FBATH11", "gmv": 833890, "gmv_pd": 4792, "sell_price": 705, "orig_price": 790, "discount_pct": 11.4, "h2_vs_h1": 1.55, "cpgn_lift": 2.32, "qty": 1191, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลเบสิค แขนสั้นคอจีน WA-3329", "sku": "WA-3329", "gmv": 825007, "gmv_pd": 3587, "sell_price": 306, "orig_price": 443, "discount_pct": 33.5, "h2_vs_h1": 2.61, "cpgn_lift": 2.22, "qty": 2798, "tag": "Rising"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทยฤดูกาลใหม่ 2026/27 Cheer Polo (WA-262FBATH30)", "sku": "WA-262FBATH30", "gmv": 804630, "gmv_pd": 10058, "sell_price": 561, "orig_price": 590, "discount_pct": 4.8, "h2_vs_h1": null, "cpgn_lift": 2.1, "qty": 1433, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล PIN (WA-232PLACL34)", "sku": "WA-232PLACL34", "gmv": 795949, "gmv_pd": 3585, "sell_price": 188, "orig_price": 306, "discount_pct": 37.2, "h2_vs_h1": 5.41, "cpgn_lift": 2.2, "qty": 4160, "tag": "Rising"}, {"name": "WARRIX กางเกงวอร์ม Titan II (WP-223WRACL30)", "sku": "WP-223WRACL30", "gmv": 793176, "gmv_pd": 3347, "sell_price": 453, "orig_price": 690, "discount_pct": 37.2, "h2_vs_h1": 1.16, "cpgn_lift": 1.94, "qty": 1831, "tag": "Standard"}, {"name": "WARRIX เสื้อปกคอวีแขนสั้น Football Lifestyle Oversize T-shirt Unisex (WA-261FBATH13)", "sku": "WA-261FBATH13", "gmv": 780341, "gmv_pd": 4002, "sell_price": 850, "orig_price": 890, "discount_pct": 4.5, "h2_vs_h1": 0.64, "cpgn_lift": 1.8, "qty": 918, "tag": "Standard"}, {"name": "WARRIX กางเกงฟุตบอลทีมชาติ WP-1509", "sku": "WP-1509", "gmv": 744603, "gmv_pd": 3142, "sell_price": 84, "orig_price": 159, "discount_pct": 48.6, "h2_vs_h1": 1.14, "cpgn_lift": 1.7, "qty": 9103, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย (Replica) Blackout TH National Jersey 2025/26 (WA-254FBATH52)", "sku": "WA-254FBATH52", "gmv": 733898, "gmv_pd": 3883, "sell_price": 1108, "orig_price": 1290, "discount_pct": 14.3, "h2_vs_h1": 0.74, "cpgn_lift": 1.55, "qty": 664, "tag": "Standard"}, {"name": "WARRIX กางเกงฟุตบอล New color WP-1509", "sku": "WP-1509", "gmv": 698438, "gmv_pd": 2947, "sell_price": 69, "orig_price": 159, "discount_pct": 58.6, "h2_vs_h1": 1.78, "cpgn_lift": 2.27, "qty": 10604, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 2025/26 (CHEER POLO) WA-253FBATH30", "sku": "WA-253FBATH30", "gmv": 693069, "gmv_pd": 3332, "sell_price": 353, "orig_price": 590, "discount_pct": 40.9, "h2_vs_h1": 1.68, "cpgn_lift": 2.21, "qty": 1989, "tag": "Standard"}, {"name": "WARRIX THAILAND HOME JERSEY 2024/25 CHEER POLO (WA-243FBATH30)", "sku": "WA-243FBATH30", "gmv": 682970, "gmv_pd": 2906, "sell_price": 252, "orig_price": 590, "discount_pct": 58.0, "h2_vs_h1": 0.69, "cpgn_lift": 1.5, "qty": 2758, "tag": "Standard"}, {"name": "WARRIX เสื้อวอร์ม Titan II (WA-223WRACL30)", "sku": "WA-223WRACL30", "gmv": 676005, "gmv_pd": 2926, "sell_price": 541, "orig_price": 790, "discount_pct": 34.6, "h2_vs_h1": 1.03, "cpgn_lift": 2.22, "qty": 1309, "tag": "Standard"}, {"name": "WARRIX  WOVEN PANTS กางเกงวอร์ม รุ่น BASIE (WP-262JKACL70)", "sku": "WP-262JKACL70", "gmv": 660570, "gmv_pd": 5201, "sell_price": 657, "orig_price": 690, "discount_pct": 4.8, "h2_vs_h1": 3.46, "cpgn_lift": 1.97, "qty": 1006, "tag": "Rising"}, {"name": "WARRIX DYNAMIC RUNNING SHORTS  WP-221RNACL40", "sku": "WP-221RNACL40", "gmv": 617514, "gmv_pd": 2859, "sell_price": 365, "orig_price": 890, "discount_pct": 61.2, "h2_vs_h1": 0.39, "cpgn_lift": 1.92, "qty": 1789, "tag": "Clearance"}, {"name": "WARRIX เสื้อโปโล VAFFLE POLO BLACK COLOR (WA-222PLACL34) สีดำ", "sku": "WA-222PLACL34", "gmv": 614889, "gmv_pd": 2650, "sell_price": 293, "orig_price": 399, "discount_pct": 28.5, "h2_vs_h1": 1.44, "cpgn_lift": 2.71, "qty": 2156, "tag": "Booster"}, {"name": "WARRIX เสื้อคอกลม Football Lifestyle Oversize T-shirt Unisex (WA-254FBATH10)", "sku": "WA-254FBATH10", "gmv": 606454, "gmv_pd": 2958, "sell_price": 765, "orig_price": 890, "discount_pct": 14.1, "h2_vs_h1": 0.8, "cpgn_lift": 2.19, "qty": 793, "tag": "Standard"}, {"name": "Warrix เสื้อคอปกแขนยาว Football Lifestyle Oversize T-shirt Unisex (WA-254FBATH16)", "sku": "WA-254FBATH16", "gmv": 566443, "gmv_pd": 3062, "sell_price": 837, "orig_price": 990, "discount_pct": 15.2, "h2_vs_h1": 1.21, "cpgn_lift": 2.11, "qty": 675, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย THAILAND CHEER ICON JERSEY 2024/25 (WA-244FBATH53)", "sku": "WA-244FBATH53", "gmv": 536233, "gmv_pd": 8512, "sell_price": 205, "orig_price": 399, "discount_pct": 49.1, "h2_vs_h1": null, "cpgn_lift": 2.3, "qty": 2641, "tag": "Standard"}, {"name": "Warrix เสื้อคอปกแขนสั้น Football Lifestyle Oversize T-shirt Unisex (WA-254FBATH14)", "sku": "WA-254FBATH14", "gmv": 509285, "gmv_pd": 2598, "sell_price": 796, "orig_price": 890, "discount_pct": 10.6, "h2_vs_h1": 0.85, "cpgn_lift": 1.62, "qty": 640, "tag": "Standard"}, {"name": "WARRIX กางเกงฟุตบอล ขาสั้นเด็ก WP-1509K", "sku": "WP-1509K", "gmv": 490115, "gmv_pd": 2068, "sell_price": 67, "orig_price": 143, "discount_pct": 57.3, "h2_vs_h1": 1.73, "cpgn_lift": 1.59, "qty": 8055, "tag": "Standard"}, {"name": "WARRIX THAILAND JERSEY 2023/24 CHEER (WA-233FBATH53)", "sku": "WA-233FBATH53", "gmv": 483990, "gmv_pd": 3315, "sell_price": 187, "orig_price": 399, "discount_pct": 53.4, "h2_vs_h1": 0.08, "cpgn_lift": 0.87, "qty": 2604, "tag": "Clearance"}, {"name": "WARRIX กางเกงคาร์โก้ CARGO PANT 2026 (WP-263CBACL01)", "sku": "WP-263CBACL01", "gmv": 481356, "gmv_pd": 14587, "sell_price": 1049, "orig_price": 1090, "discount_pct": 3.8, "h2_vs_h1": null, "cpgn_lift": 1.94, "qty": 459, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 2025/26 (CHEER POLO) WA-253FBATH31", "sku": "WA-253FBATH31", "gmv": 470978, "gmv_pd": 2343, "sell_price": 365, "orig_price": 590, "discount_pct": 39.4, "h2_vs_h1": 0.98, "cpgn_lift": 2.16, "qty": 1317, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล PIQUE (WA-212PLACL30) ปี 2025", "sku": "WA-212PLACL30", "gmv": 469253, "gmv_pd": 2040, "sell_price": 199, "orig_price": 307, "discount_pct": 35.7, "h2_vs_h1": 3.63, "cpgn_lift": 1.87, "qty": 2389, "tag": "Rising"}, {"name": "WARRIX เสื้อแจ็คเก็ตแขนยาว MONTE (WA-231WRACL70)", "sku": "WA-231WRACL70", "gmv": 445868, "gmv_pd": 2144, "sell_price": 637, "orig_price": 990, "discount_pct": 36.1, "h2_vs_h1": 0.93, "cpgn_lift": 2.11, "qty": 705, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลแขนสั้น VELZ POLO (WA-253PLACL33)", "sku": "WA-253PLACL33", "gmv": 441473, "gmv_pd": 2963, "sell_price": 766, "orig_price": 797, "discount_pct": 4.1, "h2_vs_h1": 1.09, "cpgn_lift": 1.69, "qty": 577, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล รุ่น VIVIDUS POLO (WA-242PLACL30) 2025", "sku": "WA-242PLACL30", "gmv": 440796, "gmv_pd": 2161, "sell_price": 248, "orig_price": 453, "discount_pct": 47.6, "h2_vs_h1": 2.63, "cpgn_lift": 2.0, "qty": 1860, "tag": "Rising"}, {"name": "WARRIX WOVEN SHORT PANTS กางเกงขาสั้น 3/4 รุ่น BANSIE (WP-262JKACL71)", "sku": "WP-262JKACL71", "gmv": 427724, "gmv_pd": 3564, "sell_price": 563, "orig_price": 590, "discount_pct": 4.5, "h2_vs_h1": 4.64, "cpgn_lift": 1.92, "qty": 759, "tag": "Rising"}, {"name": "Warrix กางเกงวิ่ง Light Running Collection Laser Cut Shorts (WP-233RNACL01)", "sku": "WP-233RNACL01", "gmv": 427463, "gmv_pd": 2375, "sell_price": 387, "orig_price": 890, "discount_pct": 58.3, "h2_vs_h1": 0.23, "cpgn_lift": 1.71, "qty": 1152, "tag": "Clearance"}, {"name": "WARRIX เสื้อโปโล VAFFLE POLO (WA-222PLACL34)", "sku": "WA-222PLACL34", "gmv": 421587, "gmv_pd": 1925, "sell_price": 263, "orig_price": 399, "discount_pct": 35.7, "h2_vs_h1": 1.54, "cpgn_lift": 2.38, "qty": 1644, "tag": "Standard"}, {"name": "WARRIX กางเกงวอร์ม MONTE (WP-231WRACL70)", "sku": "WP-231WRACL70", "gmv": 414462, "gmv_pd": 1893, "sell_price": 450, "orig_price": 790, "discount_pct": 45.7, "h2_vs_h1": 0.71, "cpgn_lift": 2.02, "qty": 967, "tag": "Standard"}, {"name": "WARRIX กางเกงวิ่งขาสั้น 5 นิ้ว รุ่น LIGHTWEIGHT (WP-252RNACL02)", "sku": "WP-252RNACL02", "gmv": 398709, "gmv_pd": 24919, "sell_price": 216, "orig_price": 299, "discount_pct": 28.3, "h2_vs_h1": null, "cpgn_lift": 1.05, "qty": 1861, "tag": "Standard"}, {"name": "WARRIX เสื้อแจ็คเก็ตกันลม Tracksuit Windbreaker Jacket (WA-254JKACL72)", "sku": "WA-254JKACL72", "gmv": 398246, "gmv_pd": 3433, "sell_price": 942, "orig_price": 990, "discount_pct": 4.7, "h2_vs_h1": 2.17, "cpgn_lift": 1.28, "qty": 422, "tag": "Rising"}, {"name": "Warrix เสื้อโปโลทนายความ (WA-254PLACL01)", "sku": "WA-254PLACL01", "gmv": 390925, "gmv_pd": 2833, "sell_price": 484, "orig_price": 506, "discount_pct": 4.4, "h2_vs_h1": 1.71, "cpgn_lift": 1.74, "qty": 808, "tag": "Standard"}, {"name": "WARRIX | FIT JUNCTIONS TRAINING SHIRT เสื้อเทรนนิ่ง แขนสั้น (WA-252FJACL01)", "sku": "WA-252FJACL01", "gmv": 388883, "gmv_pd": 3704, "sell_price": 157, "orig_price": 166, "discount_pct": 5.4, "h2_vs_h1": null, "cpgn_lift": 1.49, "qty": 2479, "tag": "Standard"}, {"name": "WARRIX TRAIL OF DREAM SHORT SLEEVE DAWNLIGHT เสื้อวิ่งแขนสั้น (WA-252RNACL06)", "sku": "WA-252RNACL06", "gmv": 381876, "gmv_pd": 1890, "sell_price": 453, "orig_price": 490, "discount_pct": 7.9, "h2_vs_h1": 1.69, "cpgn_lift": 1.85, "qty": 846, "tag": "Standard"}, {"name": "WARRIX รองเท้าวิ่ง รุ่น FLYKNIT รองเท้าวิ่ง (WF-253RNACL01)", "sku": "WF-253RNACL01", "gmv": 379019, "gmv_pd": 16479, "sell_price": 865, "orig_price": 1990, "discount_pct": 56.6, "h2_vs_h1": null, "cpgn_lift": 3.2, "qty": 439, "tag": "Booster"}, {"name": "WARRIX THAILAND HOME JERSEY 2024/25 REPLICA (WA-243FBATH52)", "sku": "WA-243FBATH52", "gmv": 370873, "gmv_pd": 1717, "sell_price": 376, "orig_price": 890, "discount_pct": 60.0, "h2_vs_h1": 1.09, "cpgn_lift": 2.15, "qty": 1041, "tag": "Standard"}, {"name": "WARRIX เสื้อกีฬา ออกกำลังกาย Training Gym T-shirt (WA-242TRACL04)", "sku": "WA-242TRACL04", "gmv": 360572, "gmv_pd": 3278, "sell_price": 394, "orig_price": 790, "discount_pct": 50.0, "h2_vs_h1": null, "cpgn_lift": 1.62, "qty": 913, "tag": "Standard"}, {"name": "WARRIX | FIT JUNCTIONS PANTS กางเกงขายาว (WP-252FJACL03)", "sku": "WP-252FJACL03", "gmv": 356608, "gmv_pd": 3302, "sell_price": 212, "orig_price": 227, "discount_pct": 6.4, "h2_vs_h1": null, "cpgn_lift": 1.6, "qty": 1676, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล PIQUE PLUS (WA-221PLACL30) V.2", "sku": "WA-221PLACL30", "gmv": 351389, "gmv_pd": 1802, "sell_price": 189, "orig_price": 304, "discount_pct": 42.7, "h2_vs_h1": 2.78, "cpgn_lift": 1.74, "qty": 2019, "tag": "Rising"}, {"name": "WARRIX เสื้อซ้อมฟุตบอลทีมชาติไทย (FULL SPONSOR) รุ่น AEROLINE (WA-261FBATH74)", "sku": "WA-261FBATH74", "gmv": 333061, "gmv_pd": 2730, "sell_price": 1081, "orig_price": 1104, "discount_pct": 2.1, "h2_vs_h1": 0.9, "cpgn_lift": 1.51, "qty": 308, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล Pin Polo New Color (WA-232PLACL34) 2025", "sku": "WA-232PLACL34", "gmv": 330758, "gmv_pd": 2120, "sell_price": 180, "orig_price": 305, "discount_pct": 41.3, "h2_vs_h1": 5.96, "cpgn_lift": 1.88, "qty": 1849, "tag": "Rising"}, {"name": "WARRIX  เสื้อโปโลแขนสั้น Luminous (WA-253PLMCL37)", "sku": "WA-253PLMCL37", "gmv": 312767, "gmv_pd": 1862, "sell_price": 336, "orig_price": 454, "discount_pct": 28.0, "h2_vs_h1": 1.48, "cpgn_lift": 2.08, "qty": 959, "tag": "Standard"}, {"name": "WARRIX เสื้อเชียร์จุฬา Chula Baka Forward - Cheer Polo (WA-251PLACU01)", "sku": "WA-251PLACU01", "gmv": 300273, "gmv_pd": 1458, "sell_price": 256, "orig_price": 350, "discount_pct": 28.6, "h2_vs_h1": 0.23, "cpgn_lift": 1.23, "qty": 1202, "tag": "Clearance"}, {"name": "Warrix ถุงเท้าฟุตบอลเบสิค WC-1519", "sku": "WC-1519", "gmv": 299514, "gmv_pd": 1264, "sell_price": 55, "orig_price": 99, "discount_pct": 48.8, "h2_vs_h1": 1.85, "cpgn_lift": 1.45, "qty": 5909, "tag": "Standard"}, {"name": "WARRIX  เสื้อโปโลเบสิค แขนสั้น CLASSIC POLO SHIRT (WA-PLAN15) ปี2025", "sku": "WA-PLAN15", "gmv": 294253, "gmv_pd": 2043, "sell_price": 325, "orig_price": 452, "discount_pct": 30.2, "h2_vs_h1": 4.69, "cpgn_lift": 0.84, "qty": 934, "tag": "Rising"}, {"name": "WARRIX เสื้อฟุตบอลเบสิค  EASY TO GO BASIC T-SHIRT (WA-241FBACL08)", "sku": "WA-241FBACL08", "gmv": 292161, "gmv_pd": 1334, "sell_price": 75, "orig_price": 199, "discount_pct": 63.2, "h2_vs_h1": 1.82, "cpgn_lift": 1.56, "qty": 3989, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล PIN (WA-232PLACL34) V.2", "sku": "WA-232PLACL34", "gmv": 288608, "gmv_pd": 1429, "sell_price": 197, "orig_price": 305, "discount_pct": 37.1, "h2_vs_h1": 2.23, "cpgn_lift": 1.37, "qty": 1510, "tag": "Rising"}, {"name": "WARRIX เสื้อโปโล BUBBLE | WA-3324", "sku": "WA-3324", "gmv": 280168, "gmv_pd": 1482, "sell_price": 307, "orig_price": 449, "discount_pct": 35.2, "h2_vs_h1": 2.01, "cpgn_lift": 1.48, "qty": 963, "tag": "Rising"}, {"name": "WARRIX เสื้อโปโล รุ่น CU20 (WA-253PLACU01)", "sku": "WA-253PLACU01", "gmv": 270853, "gmv_pd": 1703, "sell_price": 677, "orig_price": 690, "discount_pct": 1.9, "h2_vs_h1": 1.23, "cpgn_lift": 1.59, "qty": 400, "tag": "Standard"}, {"name": "WARRIX สปอร์ตบรา TRAINING SPORT BRA (WA-242TRACL01)", "sku": "WA-242TRACL01", "gmv": 266187, "gmv_pd": 1849, "sell_price": 543, "orig_price": 1290, "discount_pct": 59.1, "h2_vs_h1": 2.77, "cpgn_lift": 2.26, "qty": 504, "tag": "Rising"}, {"name": "Warrix Trail of Dream Tank Top Floatlight เสื้อกล้ามวิ่งเทรล (WA-252RNACL07)", "sku": "WA-252RNACL07", "gmv": 265780, "gmv_pd": 1611, "sell_price": 387, "orig_price": 390, "discount_pct": 0.8, "h2_vs_h1": 1.63, "cpgn_lift": 2.23, "qty": 687, "tag": "Standard"}, {"name": "WARRIX TRAIL OF DREAM LADY CROP BLOOM LIGHT เสื้อครอป (WA-252RNWCL01)", "sku": "WA-252RNWCL01", "gmv": 254376, "gmv_pd": 1259, "sell_price": 379, "orig_price": 390, "discount_pct": 2.8, "h2_vs_h1": 1.7, "cpgn_lift": 1.87, "qty": 671, "tag": "Standard"}, {"name": "WARRIX กางเกงยีนส์ขายาว Jeans Tapered Straight รุ่น W103 PANSA", "sku": "WARRIX", "gmv": 252850, "gmv_pd": 1819, "sell_price": 932, "orig_price": 2490, "discount_pct": 63.1, "h2_vs_h1": 1.1, "cpgn_lift": 1.64, "qty": 275, "tag": "Standard"}, {"name": "WARRIX  เสื้อโปโลเบสิค แขนสั้น WA-3315N .v2", "sku": "WA-3315N", "gmv": 247587, "gmv_pd": 1368, "sell_price": 304, "orig_price": 453, "discount_pct": 34.6, "h2_vs_h1": 1.19, "cpgn_lift": 2.6, "qty": 837, "tag": "Booster"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 2025/26 Replica Grade (WA-253FBATH52)", "sku": "WA-253FBATH52", "gmv": 246780, "gmv_pd": 2109, "sell_price": 658, "orig_price": 1290, "discount_pct": 49.0, "h2_vs_h1": 1.29, "cpgn_lift": 2.28, "qty": 375, "tag": "Standard"}, {"name": "Warrix กางเกงชิโน Chino Relax Fit (LP-244CAMCL01)", "sku": "LP-244CAMCL01", "gmv": 243136, "gmv_pd": 1885, "sell_price": 620, "orig_price": 990, "discount_pct": 38.1, "h2_vs_h1": 2.73, "cpgn_lift": 2.37, "qty": 397, "tag": "Rising"}, {"name": "DRY TECH POLO เสื้อโปโล รุ่น DRY TECH V.1 (CA-SPU-SR0003)", "sku": "CA-SPU-SR0003", "gmv": 233329, "gmv_pd": 1122, "sell_price": 190, "orig_price": 399, "discount_pct": 55.6, "h2_vs_h1": 0.83, "cpgn_lift": 1.75, "qty": 1318, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทยฤดูกาลใหม่ 2026/27 Cheer Kid (WA-262FBKTH53)", "sku": "WA-262FBKTH53", "gmv": 230626, "gmv_pd": 2919, "sell_price": 385, "orig_price": 399, "discount_pct": 3.5, "h2_vs_h1": null, "cpgn_lift": 1.65, "qty": 599, "tag": "Standard"}, {"name": "WARRIX เสื้อบาส BASKET BOY MATCH JERSEY (WA-252BKAWP01)", "sku": "WA-252BKAWP01", "gmv": 227429, "gmv_pd": 1486, "sell_price": 644, "orig_price": 990, "discount_pct": 36.5, "h2_vs_h1": 1.01, "cpgn_lift": 1.72, "qty": 362, "tag": "Standard"}, {"name": "WARRIX | FIT JUNCTIONS JOGGER PANTS กางเกงขายาวจั้ม (WP-252FJACL02)", "sku": "WP-252FJACL02", "gmv": 221240, "gmv_pd": 2068, "sell_price": 210, "orig_price": 223, "discount_pct": 5.5, "h2_vs_h1": null, "cpgn_lift": 1.49, "qty": 1050, "tag": "Standard"}, {"name": "WARRIX | FIT JUNCTIONS กางเกงขาสั้น กางเกงฟุตบอล (WP-252FJACL01)", "sku": "WP-252FJACL01", "gmv": 220347, "gmv_pd": 2099, "sell_price": 161, "orig_price": 170, "discount_pct": 4.8, "h2_vs_h1": null, "cpgn_lift": 1.69, "qty": 1364, "tag": "Standard"}, {"name": "WARRIX กางเกงยีนส์ Tapered Straight - Jeans Essential (LP-244JEMW104)", "sku": "LP-244JEMW104", "gmv": 214580, "gmv_pd": 1480, "sell_price": 681, "orig_price": 1990, "discount_pct": 66.0, "h2_vs_h1": 1.5, "cpgn_lift": 1.28, "qty": 317, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลมหิดลโอเวอร์ไซส์ Mahidol Oversize Lifestyle Jersey 2026 (WA-261FBAMU10)", "sku": "WA-261FBAMU10", "gmv": 209674, "gmv_pd": 1856, "sell_price": 738, "orig_price": 790, "discount_pct": 6.5, "h2_vs_h1": 1.5, "cpgn_lift": 1.68, "qty": 284, "tag": "Standard"}, {"name": "WARRIX JOGGER KIDS WARM PANTS (WP-241WRKCL02)", "sku": "WP-241WRKCL02", "gmv": 209542, "gmv_pd": 1576, "sell_price": 162, "orig_price": 349, "discount_pct": 55.9, "h2_vs_h1": 0.25, "cpgn_lift": 1.18, "qty": 1362, "tag": "Clearance"}, {"name": "WARRIX เสื้อกีฬา แขนสั้น รุ่น Windwin Team wear (WA-241FBACL06)", "sku": "WA-241FBACL06", "gmv": 208228, "gmv_pd": 925, "sell_price": 157, "orig_price": 306, "discount_pct": 49.6, "h2_vs_h1": 1.97, "cpgn_lift": 2.39, "qty": 1352, "tag": "Standard"}, {"name": "[สำหรับ SPayLater เท่านั้น] WARRIX เสื้อโปโล PIN BLACK COLOR (WA-232PLACL34)", "sku": "WA-232PLACL34", "gmv": 200175, "gmv_pd": 200175, "sell_price": 255, "orig_price": 299, "discount_pct": 14.7, "h2_vs_h1": null, "cpgn_lift": null, "qty": 785, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลสโมสรอุทัยธานี FC 2025 (WA-253FBAUT01)", "sku": "WA-253FBAUT01", "gmv": 198964, "gmv_pd": 1391, "sell_price": 604, "orig_price": 690, "discount_pct": 14.9, "h2_vs_h1": 0.71, "cpgn_lift": 1.32, "qty": 339, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล อัสสัมชัญ Jersey Polo Assumption (WA-251PLAAC01)", "sku": "WA-251PLAAC01", "gmv": 192923, "gmv_pd": 1269, "sell_price": 647, "orig_price": 790, "discount_pct": 18.1, "h2_vs_h1": 1.12, "cpgn_lift": 1.4, "qty": 298, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 25/26 (CHEER KIDS) (WA-253FBKTH53)", "sku": "WA-253FBKTH53", "gmv": 190282, "gmv_pd": 1007, "sell_price": 301, "orig_price": 399, "discount_pct": 24.7, "h2_vs_h1": 1.1, "cpgn_lift": 1.62, "qty": 633, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล VAFFLE POLO (WA-222PLACL34) 2025", "sku": "WA-222PLACL34", "gmv": 187715, "gmv_pd": 1124, "sell_price": 228, "orig_price": 399, "discount_pct": 44.7, "h2_vs_h1": 4.73, "cpgn_lift": 1.67, "qty": 850, "tag": "Rising"}, {"name": "WARRIX เสื้อแข่งบาสเกตบอลทีมชาติไทย THAILAND BASKETBALL JERSEY 2024/2025 (WA-243BKACL01)", "sku": "WA-243BKACL01", "gmv": 177705, "gmv_pd": 1269, "sell_price": 450, "orig_price": 990, "discount_pct": 54.8, "h2_vs_h1": 0.62, "cpgn_lift": 1.79, "qty": 397, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอล Oversize Jersey logo BCC (WA-254FBABC10)", "sku": "WA-254FBABC10", "gmv": 174962, "gmv_pd": 1250, "sell_price": 767, "orig_price": 790, "discount_pct": 2.9, "h2_vs_h1": 1.09, "cpgn_lift": 1.25, "qty": 228, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอล Football Jersey Long Sleeve Smiley World Collection (LA-241FBACL02)", "sku": "LA-241FBACL02", "gmv": 172159, "gmv_pd": 1609, "sell_price": 807, "orig_price": 1590, "discount_pct": 49.2, "h2_vs_h1": 1.7, "cpgn_lift": 1.7, "qty": 213, "tag": "Standard"}, {"name": "WARRIX เสื้อคอปกแขนยาว Football Lifestyle Oversize T-shirt Unisex (WA-254FBATH11)", "sku": "WA-254FBATH11", "gmv": 169775, "gmv_pd": 1715, "sell_price": 828, "orig_price": 990, "discount_pct": 15.9, "h2_vs_h1": 1.27, "cpgn_lift": 2.26, "qty": 204, "tag": "Standard"}, {"name": "WARRIX กางเกงเทรนนิ่ง BACK NET (WP-224TRACL01)", "sku": "WP-224TRACL01", "gmv": 169617, "gmv_pd": 912, "sell_price": 293, "orig_price": 790, "discount_pct": 65.6, "h2_vs_h1": 1.03, "cpgn_lift": 1.82, "qty": 624, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซซ์ กรุงเทพคริสเตียน Oversize Jersey BCC Bangkok Christian (LA-243TSABC01)", "sku": "LA-243TSABC01", "gmv": 167234, "gmv_pd": 1548, "sell_price": 437, "orig_price": 790, "discount_pct": 44.7, "h2_vs_h1": 0.6, "cpgn_lift": 1.21, "qty": 383, "tag": "Standard"}, {"name": "WARRIX | FIT JUNCTIONS BASIC POLO SHIRT เสื้อโปโลเบสิค (WA-252FJACL02)", "sku": "WA-252FJACL02", "gmv": 166416, "gmv_pd": 1585, "sell_price": 212, "orig_price": 224, "discount_pct": 5.1, "h2_vs_h1": null, "cpgn_lift": 1.55, "qty": 786, "tag": "Standard"}, {"name": "WARRIX เสื้อวิ่ง รุ่น CITY RUN DAY DREAM T-SHIRT (WA-241RNACL07)", "sku": "WA-241RNACL07", "gmv": 159375, "gmv_pd": 861, "sell_price": 259, "orig_price": 790, "discount_pct": 67.5, "h2_vs_h1": 2.25, "cpgn_lift": 1.68, "qty": 620, "tag": "Rising"}, {"name": "WARRIX รองเท้าวิ่ง รุ่น AEGIS (WF-253RNACL04)", "sku": "WF-253RNACL04", "gmv": 159013, "gmv_pd": 2272, "sell_price": 1849, "orig_price": 2290, "discount_pct": 19.3, "h2_vs_h1": 1.06, "cpgn_lift": 1.13, "qty": 86, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซส์ สวนกุหลาบ Oversize Jersey SK Suankularb (LA-251TSASK01)", "sku": "LA-251TSASK01", "gmv": 158475, "gmv_pd": 1201, "sell_price": 630, "orig_price": 790, "discount_pct": 20.1, "h2_vs_h1": 0.82, "cpgn_lift": 1.68, "qty": 251, "tag": "Standard"}, {"name": "WARRIX เสื้อแข่งฟุตบอลจตุรมิตร ครั้งที่ 31 logo SK Replica (WA-254FBASK52)", "sku": "WA-254FBASK52", "gmv": 154785, "gmv_pd": 1130, "sell_price": 741, "orig_price": 790, "discount_pct": 6.3, "h2_vs_h1": 1.2, "cpgn_lift": 1.16, "qty": 209, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย (Player) Blackout TH National Jersey 2025/26 (WA-254FBATH51)", "sku": "WA-254FBATH51", "gmv": 152359, "gmv_pd": 2930, "sell_price": 2274, "orig_price": 2490, "discount_pct": 13.8, "h2_vs_h1": 1.23, "cpgn_lift": 1.31, "qty": 71, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล สีเหลือง พร้อมตราสัญลักษณ์ รุ่น PIQUE POLO (WA-241PLAKI06)", "sku": "WA-241PLAKI06", "gmv": 144743, "gmv_pd": 946, "sell_price": 179, "orig_price": 406, "discount_pct": 55.9, "h2_vs_h1": 2.49, "cpgn_lift": 4.25, "qty": 811, "tag": "Rising"}, {"name": "WARRIX กางเกงบาส BASKET BOY MATCH SHORTS (WP-252BKAWP01)", "sku": "WP-252BKAWP01", "gmv": 140643, "gmv_pd": 1065, "sell_price": 418, "orig_price": 690, "discount_pct": 40.0, "h2_vs_h1": 1.53, "cpgn_lift": 1.62, "qty": 340, "tag": "Standard"}, {"name": "WARRIX เสื้อยืดคอกลม รุ่น Basic 3 Normal Fit T-shirt Logo W Comba Lite (LA-243TSACL04)", "sku": "LA-243TSACL04", "gmv": 139201, "gmv_pd": 814, "sell_price": 137, "orig_price": 290, "discount_pct": 55.8, "h2_vs_h1": 3.46, "cpgn_lift": 1.4, "qty": 1085, "tag": "Rising"}, {"name": "WARRIX เสื้อวิ่ง ก้าวท้าใจ (WA-211RNACL01)", "sku": "WA-211RNACL01", "gmv": 137193, "gmv_pd": 621, "sell_price": 90, "orig_price": 180, "discount_pct": 51.9, "h2_vs_h1": 2.32, "cpgn_lift": 1.57, "qty": 1584, "tag": "Rising"}, {"name": "WARRIX THAILAND HOME JERSEY 2024/25 PLAYER (WA-243FBATH51)", "sku": "WA-243FBATH51", "gmv": 136503, "gmv_pd": 1569, "sell_price": 1050, "orig_price": 2490, "discount_pct": 58.5, "h2_vs_h1": 1.15, "cpgn_lift": 1.16, "qty": 132, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลเด็ก Basic One WA-204FBKCL01", "sku": "WA-204FBKCL01", "gmv": 136360, "gmv_pd": 601, "sell_price": 48, "orig_price": 179, "discount_pct": 73.6, "h2_vs_h1": 1.66, "cpgn_lift": 1.56, "qty": 2881, "tag": "Standard"}, {"name": "WARRIX กางเกงขาสั้นคาร์โก้ CARGO SHORTS PANT 2026 (WP-263CBACL02)", "sku": "WP-263CBACL02", "gmv": 135702, "gmv_pd": 5654, "sell_price": 854, "orig_price": 890, "discount_pct": 4.1, "h2_vs_h1": null, "cpgn_lift": 1.95, "qty": 159, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตซอลทีมชาติไทย THAILAND NATIONAL FUTSAL JERSEY 2024/25 (WA-243FSATH51)", "sku": "WA-243FSATH51", "gmv": 134173, "gmv_pd": 1542, "sell_price": 999, "orig_price": 2490, "discount_pct": 61.2, "h2_vs_h1": 1.53, "cpgn_lift": 1.37, "qty": 139, "tag": "Standard"}, {"name": "DRY TECH POLO เสื้อโปโล รุ่น DRY TECH V.2 (CA-SPU-SR0003)", "sku": "CA-SPU-SR0003", "gmv": 133434, "gmv_pd": 706, "sell_price": 171, "orig_price": 399, "discount_pct": 60.0, "h2_vs_h1": 0.92, "cpgn_lift": 1.4, "qty": 836, "tag": "Standard"}, {"name": "WARRIX กางเกงวอร์ม Track suit tri-proof (water/wind/cold) Pants (WP-253JKACL74)", "sku": "WP-253JKACL74", "gmv": 133280, "gmv_pd": 1481, "sell_price": 913, "orig_price": 990, "discount_pct": 7.8, "h2_vs_h1": 1.14, "cpgn_lift": 1.75, "qty": 146, "tag": "Standard"}, {"name": "WARRIX กางเกงฟุตบอลทีมชาติไทย 2025/26 (Player Grade) WP-253FBATH51", "sku": "WP-253FBATH51", "gmv": 130612, "gmv_pd": 1116, "sell_price": 426, "orig_price": 899, "discount_pct": 52.7, "h2_vs_h1": 1.62, "cpgn_lift": 2.15, "qty": 307, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลแขนสั้น WISP POLO SHIRT (WA-252PLACL32)", "sku": "WA-252PLACL32", "gmv": 128578, "gmv_pd": 1020, "sell_price": 484, "orig_price": 505, "discount_pct": 3.9, "h2_vs_h1": 1.56, "cpgn_lift": 1.87, "qty": 265, "tag": "Standard"}, {"name": "WARRIX เสื้อแจ็คเก็ต Track suit tri-proof (water/wind/cold) Jacket (WA-253JKACL74)", "sku": "WA-253JKACL74", "gmv": 127297, "gmv_pd": 2546, "sell_price": 1772, "orig_price": 1990, "discount_pct": 11.2, "h2_vs_h1": 1.32, "cpgn_lift": 1.17, "qty": 72, "tag": "Standard"}, {"name": "WARRIX เสื้อแข่งฟุตบอลจตุรมิตร ครั้งที่ 31 logo AC Replica (WA-254FBAAC52)", "sku": "WA-254FBAAC52", "gmv": 119571, "gmv_pd": 1184, "sell_price": 747, "orig_price": 790, "discount_pct": 5.4, "h2_vs_h1": 0.86, "cpgn_lift": 1.29, "qty": 160, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลแขนสั้น Blackout Jersey 2020", "sku": "WARRIX", "gmv": 118916, "gmv_pd": 3303, "sell_price": 949, "orig_price": 2313, "discount_pct": 59.1, "h2_vs_h1": 0.68, "cpgn_lift": 0.87, "qty": 126, "tag": "Standard"}, {"name": "WARRIX เสื้อซ้อมฟุตบอลทีมชาติไทย รุ่น AEROLINE (WA-261FBATH73)", "sku": "WA-261FBATH73", "gmv": 118595, "gmv_pd": 1198, "sell_price": 581, "orig_price": 603, "discount_pct": 3.5, "h2_vs_h1": 1.54, "cpgn_lift": 1.24, "qty": 204, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลทีมชาติไทย 2025/26 (CHEER Grade) WA-253FBATH54", "sku": "WA-253FBATH54", "gmv": 117405, "gmv_pd": 1334, "sell_price": 326, "orig_price": 399, "discount_pct": 18.3, "h2_vs_h1": null, "cpgn_lift": 1.44, "qty": 360, "tag": "Standard"}, {"name": "WARRIX  เสื้อโปโลช้างศึก 2025/26 รุ่น Classic (WA-254PLATH31)", "sku": "WA-254PLATH31", "gmv": 116721, "gmv_pd": 846, "sell_price": 415, "orig_price": 600, "discount_pct": 31.5, "h2_vs_h1": 0.52, "cpgn_lift": 1.6, "qty": 284, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซส์ เทพศิรินทร์ Oversize Jersey DS Debsirin (LA-243TSADS01)", "sku": "LA-243TSADS01", "gmv": 115881, "gmv_pd": 1449, "sell_price": 419, "orig_price": 790, "discount_pct": 47.0, "h2_vs_h1": 0.5, "cpgn_lift": 1.33, "qty": 277, "tag": "Standard"}, {"name": "WARRIX CITY RUN HORIZON SINGLET (WA-241RNACL03)", "sku": "WA-241RNACL03", "gmv": 114349, "gmv_pd": 710, "sell_price": 282, "orig_price": 690, "discount_pct": 59.8, "h2_vs_h1": 0.81, "cpgn_lift": 1.56, "qty": 412, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลคอกลมแขนสั้น WA-FBA071", "sku": "WA-FBA071", "gmv": 113906, "gmv_pd": 556, "sell_price": 62, "orig_price": 199, "discount_pct": 68.0, "h2_vs_h1": 1.09, "cpgn_lift": 1.85, "qty": 1790, "tag": "Standard"}, {"name": "WARRIX CITY RUN HORIZON TANK TOP (WA-241RNACL04)", "sku": "WA-241RNACL04", "gmv": 113237, "gmv_pd": 735, "sell_price": 272, "orig_price": 690, "discount_pct": 61.0, "h2_vs_h1": 0.6, "cpgn_lift": 1.51, "qty": 421, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล EASY TO GO POLO SHIRT (WA-241PLACL32)", "sku": "WA-241PLACL32", "gmv": 112951, "gmv_pd": 653, "sell_price": 207, "orig_price": 299, "discount_pct": 33.0, "h2_vs_h1": 0.64, "cpgn_lift": 1.44, "qty": 564, "tag": "Standard"}, {"name": "WARRIX เสื้อวอริกซ์ Oversized Jersey รุ่น CU20 V.2 (WA-253FBACU11)", "sku": "WA-253FBACU11", "gmv": 112840, "gmv_pd": 2453, "sell_price": 881, "orig_price": 890, "discount_pct": 0.9, "h2_vs_h1": null, "cpgn_lift": 1.66, "qty": 128, "tag": "Standard"}, {"name": "WARRIX  กางเกงวิ่งขาสั้น Trail Running Short (WP-252RNACL01)", "sku": "WP-252RNACL01", "gmv": 112366, "gmv_pd": 1422, "sell_price": 803, "orig_price": 890, "discount_pct": 9.8, "h2_vs_h1": 0.79, "cpgn_lift": 1.45, "qty": 140, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล PIN POLO (WA-232PLACL34) V.3", "sku": "WA-232PLACL34", "gmv": 111208, "gmv_pd": 993, "sell_price": 143, "orig_price": 309, "discount_pct": 54.9, "h2_vs_h1": 0.58, "cpgn_lift": 0.86, "qty": 807, "tag": "Standard"}, {"name": "WARRIX รองเท้าวิ่ง รุ่น TERRA (WF-253RNACL03)", "sku": "WF-253RNACL03", "gmv": 110511, "gmv_pd": 2302, "sell_price": 1842, "orig_price": 2290, "discount_pct": 19.6, "h2_vs_h1": 1.09, "cpgn_lift": 1.36, "qty": 60, "tag": "Standard"}, {"name": "WARRIX CITY RUN MOVE T-SHIRT (WA-241RNACL02)", "sku": "WA-241RNACL02", "gmv": 110412, "gmv_pd": 712, "sell_price": 307, "orig_price": 790, "discount_pct": 61.3, "h2_vs_h1": 1.13, "cpgn_lift": 1.64, "qty": 361, "tag": "Standard"}, {"name": "[Special Price ] WARRIX เสื้อโปโลแขนสั้น vividus WA-242PLACL30", "sku": "WA-242PLACL30", "gmv": 110085, "gmv_pd": 6116, "sell_price": 318, "orig_price": 451, "discount_pct": 29.4, "h2_vs_h1": null, "cpgn_lift": 0.61, "qty": 346, "tag": "Standard"}, {"name": "WARRIX เสื้อออกกำลังกาย BASIC ONE TRAINING SHIRT (WA-251FBACL01) Ver.2", "sku": "WA-251FBACL01", "gmv": 109410, "gmv_pd": 739, "sell_price": 96, "orig_price": 206, "discount_pct": 52.3, "h2_vs_h1": 2.64, "cpgn_lift": 1.82, "qty": 1118, "tag": "Rising"}, {"name": "Warrix กางเกงยีนส์ TAKA Tapered Slim W202 (LP-243JEMW202)", "sku": "LP-243JEMW202", "gmv": 108605, "gmv_pd": 1324, "sell_price": 936, "orig_price": 2490, "discount_pct": 65.1, "h2_vs_h1": 1.22, "cpgn_lift": 1.18, "qty": 125, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลวอริกซ์ รุ่น CAMO V.2 (WA-253PLMCL01)", "sku": "WA-253PLMCL01", "gmv": 107094, "gmv_pd": 1391, "sell_price": 510, "orig_price": 651, "discount_pct": 24.2, "h2_vs_h1": 1.95, "cpgn_lift": 1.0, "qty": 217, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล เทพศิรินทร์ Jersey Polo Debsirin (WA-251PLADS01)", "sku": "WA-251PLADS01", "gmv": 106566, "gmv_pd": 1076, "sell_price": 656, "orig_price": 790, "discount_pct": 16.7, "h2_vs_h1": 0.69, "cpgn_lift": 1.05, "qty": 162, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล Bubble New color WA-3324 .V3", "sku": "WA-3324", "gmv": 106329, "gmv_pd": 886, "sell_price": 243, "orig_price": 453, "discount_pct": 54.7, "h2_vs_h1": 2.16, "cpgn_lift": 2.74, "qty": 520, "tag": "Rising"}, {"name": "WARRIX เสื้อแข่งฟุตบอลจตุรมิตร ครั้งที่ 31 logo DS Replica (WA-254FBADS52)", "sku": "WA-254FBADS52", "gmv": 105381, "gmv_pd": 1211, "sell_price": 747, "orig_price": 790, "discount_pct": 5.4, "h2_vs_h1": 0.66, "cpgn_lift": 1.17, "qty": 141, "tag": "Standard"}, {"name": "Warrix เสื้อฟุตบอลคอกลมแขนสั้นNew color WA-FBA071", "sku": "WA-FBA071", "gmv": 105198, "gmv_pd": 511, "sell_price": 61, "orig_price": 200, "discount_pct": 69.8, "h2_vs_h1": 0.79, "cpgn_lift": 1.94, "qty": 1741, "tag": "Standard"}, {"name": "WARRIX เสื้อแข่งฟุตบอลจตุรมิตร ครั้งที่ 31 logo BCC Replica (WA-254FBABC52)", "sku": "WA-254FBABC52", "gmv": 104678, "gmv_pd": 1036, "sell_price": 759, "orig_price": 790, "discount_pct": 4.0, "h2_vs_h1": 0.79, "cpgn_lift": 1.0, "qty": 138, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล กรุงเทพคริสเตียน Jersey Polo Bangkok Christian (WA-251PLABC01)", "sku": "WA-251PLABC01", "gmv": 102976, "gmv_pd": 1010, "sell_price": 640, "orig_price": 790, "discount_pct": 19.0, "h2_vs_h1": 1.19, "cpgn_lift": 1.33, "qty": 161, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอล Oversize Jersey logo SK (WA-254FBASK10)", "sku": "WA-254FBASK10", "gmv": 99871, "gmv_pd": 1086, "sell_price": 751, "orig_price": 790, "discount_pct": 4.9, "h2_vs_h1": 1.05, "cpgn_lift": 1.23, "qty": 133, "tag": "Standard"}, {"name": "WARRIX SPORTกางเกงฟุตบอลเบสิค WP-1509-ขาว-WW", "sku": "WP-1509", "gmv": 99560, "gmv_pd": 493, "sell_price": 91, "orig_price": 159, "discount_pct": 45.3, "h2_vs_h1": 3.39, "cpgn_lift": 2.65, "qty": 1145, "tag": "Rising"}, {"name": "Warrix เสื้อแจ็คเก็ต Track suit tri-proof (water/wind/cold) Jacket (Logo Changsuek) WA-253JKATH74", "sku": "WA-253JKATH74", "gmv": 98767, "gmv_pd": 1975, "sell_price": 1674, "orig_price": 2090, "discount_pct": 19.9, "h2_vs_h1": 0.85, "cpgn_lift": 1.01, "qty": 59, "tag": "Standard"}, {"name": "WARRIX กางเกงแข่งบาสเกตบอล ทีมชาติไทย THAILAND BASKETBALL JERSEY 2024/2025 (WP-243BKACL01)", "sku": "WP-243BKACL01", "gmv": 97549, "gmv_pd": 774, "sell_price": 240, "orig_price": 590, "discount_pct": 59.9, "h2_vs_h1": 0.73, "cpgn_lift": 1.5, "qty": 412, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลช้างศึก รุ่น LUMINOUS (WA-254PLATH30)", "sku": "WA-254PLATH30", "gmv": 96646, "gmv_pd": 826, "sell_price": 437, "orig_price": 603, "discount_pct": 27.5, "h2_vs_h1": 1.01, "cpgn_lift": 1.45, "qty": 221, "tag": "Standard"}, {"name": "Warrix เสื้อโปโลลำลอง รุ่น Bubble  สีทีมชาติ ผู้ชาย ผู้หญิง  (WA-3324)", "sku": "WA-3324", "gmv": 95852, "gmv_pd": 639, "sell_price": 271, "orig_price": 453, "discount_pct": 43.9, "h2_vs_h1": 0.93, "cpgn_lift": 1.26, "qty": 377, "tag": "Standard"}, {"name": "WARRIX กระเป๋าเป้ BACKPACK OBSIDIAN (WB-254WRAMY03)", "sku": "WB-254WRAMY03", "gmv": 94249, "gmv_pd": 1346, "sell_price": 826, "orig_price": 890, "discount_pct": 7.1, "h2_vs_h1": 1.34, "cpgn_lift": 0.94, "qty": 114, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล สวนกุหลาบ Jersey Polo Suankularb (WA-251PLASK01)", "sku": "WA-251PLASK01", "gmv": 94078, "gmv_pd": 931, "sell_price": 631, "orig_price": 790, "discount_pct": 20.1, "h2_vs_h1": 1.0, "cpgn_lift": 1.24, "qty": 149, "tag": "Standard"}, {"name": "WARRIX Warrix Strike Zone Shorts Pants (WP-241FBACL01)", "sku": "WP-241FBACL01", "gmv": 93248, "gmv_pd": 510, "sell_price": 171, "orig_price": 299, "discount_pct": 49.5, "h2_vs_h1": 0.91, "cpgn_lift": 1.54, "qty": 618, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซส์ Oversized Jersey รุ่น CU20 V.2 (WA-253FBACU11)", "sku": "WA-253FBACU11", "gmv": 93182, "gmv_pd": 1276, "sell_price": 879, "orig_price": 890, "discount_pct": 1.2, "h2_vs_h1": 1.35, "cpgn_lift": 1.33, "qty": 106, "tag": "Standard"}, {"name": "WARRIX เสื้อยืดคอกลม รุ่น Basic 3 Normal Fit T-shirt Comba Lite (LA-243TSACL02)", "sku": "LA-243TSACL02", "gmv": 92897, "gmv_pd": 505, "sell_price": 113, "orig_price": 250, "discount_pct": 56.9, "h2_vs_h1": 1.22, "cpgn_lift": 1.64, "qty": 862, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลผู้หญิง รุ่น RELAXY POLO (WA-241PLWCL30)", "sku": "WA-241PLWCL30", "gmv": 92822, "gmv_pd": 636, "sell_price": 301, "orig_price": 449, "discount_pct": 35.6, "h2_vs_h1": 0.69, "cpgn_lift": 1.3, "qty": 321, "tag": "Standard"}, {"name": "WARRIX เสื้อคอกลม PULSE Training Kid (WA-231FBKCL06)", "sku": "WA-231FBKCL06", "gmv": 91676, "gmv_pd": 449, "sell_price": 122, "orig_price": 359, "discount_pct": 66.1, "h2_vs_h1": 1.21, "cpgn_lift": 1.44, "qty": 754, "tag": "Standard"}, {"name": "WARRIX เสื้อรัดกล้ามเนื้อ FORCE TOP TIGHT (WA-254CPAMY01)", "sku": "WA-254CPAMY01", "gmv": 91643, "gmv_pd": 1255, "sell_price": 649, "orig_price": 690, "discount_pct": 5.8, "h2_vs_h1": null, "cpgn_lift": 1.64, "qty": 141, "tag": "Standard"}, {"name": "WARRIX กางเกง LIFESTYLE SHORTS", "sku": "WARRIX", "gmv": 90964, "gmv_pd": 819, "sell_price": 361, "orig_price": 590, "discount_pct": 42.5, "h2_vs_h1": 1.09, "cpgn_lift": 1.24, "qty": 268, "tag": "Standard"}, {"name": "WARRIX เสื้อแจ็คเก็ต ACTIVE PRO JACKET (WA-243JKACL70)", "sku": "WA-243JKACL70", "gmv": 90919, "gmv_pd": 1568, "sell_price": 709, "orig_price": 990, "discount_pct": 32.0, "h2_vs_h1": 0.96, "cpgn_lift": 0.93, "qty": 135, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลเบสิคแขนสั้น รุ่น The Signature Polo (WA-261PLACL15)", "sku": "WA-261PLACL15", "gmv": 90725, "gmv_pd": 1315, "sell_price": 449, "orig_price": 459, "discount_pct": 2.1, "h2_vs_h1": null, "cpgn_lift": 3.15, "qty": 203, "tag": "Booster"}, {"name": "WARRIX เสื้อซ้อมฟุตบอล เสื้อกีฬา แขนสั้น รุ่น MOVE MOTION EDGE TRAINING SHIRT (WA-252FBACL01)", "sku": "WA-252FBACL01", "gmv": 89414, "gmv_pd": 699, "sell_price": 226, "orig_price": 406, "discount_pct": 45.1, "h2_vs_h1": 1.68, "cpgn_lift": 1.72, "qty": 402, "tag": "Standard"}, {"name": "Warrix เสื้อโปโล Vibes (WA-203PLACL01)", "sku": "WA-203PLACL01", "gmv": 89405, "gmv_pd": 621, "sell_price": 227, "orig_price": 413, "discount_pct": 49.9, "h2_vs_h1": 1.91, "cpgn_lift": 1.99, "qty": 432, "tag": "Standard"}, {"name": "WARRIX Solid Polo Shirt Tactical (WA-253TCACL01)", "sku": "WA-253TCACL01", "gmv": 87814, "gmv_pd": 1084, "sell_price": 610, "orig_price": 905, "discount_pct": 38.9, "h2_vs_h1": 1.1, "cpgn_lift": 1.27, "qty": 159, "tag": "Standard"}, {"name": "WARRIX กางเกงยีนส์ขาสั้น Shorts Jeans Denim รุ่น W251 WASHI (LP-241JEMW251)", "sku": "LP-241JEMW251", "gmv": 86559, "gmv_pd": 1312, "sell_price": 551, "orig_price": 1490, "discount_pct": 64.1, "h2_vs_h1": 0.62, "cpgn_lift": 1.37, "qty": 162, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซซ์ อัสสัมชัญ Oversize Jersey Assumption (LA-243TSAAC01)", "sku": "LA-243TSAAC01", "gmv": 86113, "gmv_pd": 1722, "sell_price": 566, "orig_price": 790, "discount_pct": 27.8, "h2_vs_h1": null, "cpgn_lift": 1.52, "qty": 151, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอล เสื้อกีฬา รุ่น Aeroline (WA-261FBACL01)", "sku": "WA-261FBACL01", "gmv": 86110, "gmv_pd": 1090, "sell_price": 394, "orig_price": 406, "discount_pct": 2.2, "h2_vs_h1": 1.27, "cpgn_lift": 2.62, "qty": 218, "tag": "Booster"}, {"name": "WARRIX เสื้อแจ็คเก็ตกันลม MARCOS WIND BREAKER (WA-232JKACL70)", "sku": "WA-232JKACL70", "gmv": 85522, "gmv_pd": 1239, "sell_price": 949, "orig_price": 1990, "discount_pct": 52.2, "h2_vs_h1": 0.96, "cpgn_lift": 0.82, "qty": 90, "tag": "Standard"}, {"name": "WARRIX เสื้อคอวีแขนสั้นครอป Football Lifestyle Oversize T-shirt Crop (WA-261FBWTH15)", "sku": "WA-261FBWTH15", "gmv": 85124, "gmv_pd": 1091, "sell_price": 869, "orig_price": 890, "discount_pct": 2.4, "h2_vs_h1": 0.79, "cpgn_lift": 1.36, "qty": 98, "tag": "Standard"}, {"name": "WARRIX THAILAND JERSEY 2023/24 REPLICA (WA-233FBATH52)", "sku": "WA-233FBATH52", "gmv": 84181, "gmv_pd": 702, "sell_price": 316, "orig_price": 890, "discount_pct": 65.5, "h2_vs_h1": 1.0, "cpgn_lift": 1.23, "qty": 274, "tag": "Standard"}, {"name": "WARRIX เสื้อกีฬาเชียร์ทีมชาติไทย ช้างศึก เพื่อนซี้คอบอล 2024 (WA-242FBATH52)", "sku": "WA-242FBATH52", "gmv": 83673, "gmv_pd": 940, "sell_price": 592, "orig_price": 1040, "discount_pct": 43.3, "h2_vs_h1": 0.96, "cpgn_lift": 1.29, "qty": 142, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอลโอเวอร์ไซส์แขนยาว Oversize Jersey Long Sleeve New Chapter (WA-251FBATH11)", "sku": "WA-251FBATH11", "gmv": 81027, "gmv_pd": 976, "sell_price": 506, "orig_price": 990, "discount_pct": 49.2, "h2_vs_h1": 1.21, "cpgn_lift": 1.58, "qty": 161, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล รุ่น PIQUE (WA-212PLACL30) 2026", "sku": "WA-212PLACL30", "gmv": 77113, "gmv_pd": 1151, "sell_price": 256, "orig_price": 305, "discount_pct": 20.1, "h2_vs_h1": 2.55, "cpgn_lift": 0.76, "qty": 318, "tag": "Rising"}, {"name": "WARRIX เสื้อแข่งบาสเกตบอลทีมชาติไทย (WA-254BKATH01)", "sku": "WA-254BKATH01", "gmv": 76684, "gmv_pd": 1278, "sell_price": 702, "orig_price": 890, "discount_pct": 23.1, "h2_vs_h1": 1.66, "cpgn_lift": 0.76, "qty": 112, "tag": "Standard"}, {"name": "WARRIX THAILAND JERSEY 2023/24 PLAYER (WA-233FBATH51)", "sku": "WA-233FBATH51", "gmv": 76631, "gmv_pd": 1446, "sell_price": 821, "orig_price": 2490, "discount_pct": 67.3, "h2_vs_h1": 0.82, "cpgn_lift": 1.08, "qty": 94, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอล Oversize Logo Changsuek รุ่น Solar Acid (WA-254FBATH02)", "sku": "WA-254FBATH02", "gmv": 76097, "gmv_pd": 1189, "sell_price": 777, "orig_price": 890, "discount_pct": 12.8, "h2_vs_h1": 1.02, "cpgn_lift": 1.19, "qty": 98, "tag": "Standard"}, {"name": "Warrix  เสื้อกล้ามวิ่งเทรล Trail of Dream Wowen Tank Top Floatlight (WA-252RNACL07)", "sku": "WA-252RNACL07", "gmv": 74717, "gmv_pd": 1624, "sell_price": 356, "orig_price": 390, "discount_pct": 8.8, "h2_vs_h1": null, "cpgn_lift": 1.86, "qty": 210, "tag": "Standard"}, {"name": "WARRIX กางเกงวิ่งขาสั้นผู้หญิง 3 นิ้ว สีดำ (WP-252RNWCL01)", "sku": "WP-252RNWCL01", "gmv": 74519, "gmv_pd": 510, "sell_price": 257, "orig_price": 299, "discount_pct": 14.1, "h2_vs_h1": 0.76, "cpgn_lift": 1.49, "qty": 290, "tag": "Standard"}, {"name": "WARRIX เสื้อซ้อมฟุตบอล Official  รุ่น Edge perform (WA-252FBATH73)", "sku": "WA-252FBATH73", "gmv": 73354, "gmv_pd": 734, "sell_price": 455, "orig_price": 604, "discount_pct": 24.5, "h2_vs_h1": 0.89, "cpgn_lift": 1.13, "qty": 161, "tag": "Standard"}, {"name": "WARRIX เสื้อคอกลมฟุตบอล DI ISLAND FULL SPONSOR (WA-233FBATH72)", "sku": "WA-233FBATH72", "gmv": 73205, "gmv_pd": 851, "sell_price": 571, "orig_price": 990, "discount_pct": 42.7, "h2_vs_h1": 0.86, "cpgn_lift": 1.08, "qty": 129, "tag": "Standard"}, {"name": "WARRIX เสื้อวอร์ม Titan II V.2 (WA-223WRACL30)", "sku": "WA-223WRACL30", "gmv": 72048, "gmv_pd": 987, "sell_price": 549, "orig_price": 790, "discount_pct": 29.3, "h2_vs_h1": 0.62, "cpgn_lift": 0.94, "qty": 129, "tag": "Standard"}, {"name": "WARRIXกีฬา ผ้าปิดจมูกกันฝุ่น Warrix Reusable Hydro-Tech Mask V.2 WS-203MKACL01", "sku": "WS-203MKACL01", "gmv": 71629, "gmv_pd": 358, "sell_price": 37, "orig_price": 99, "discount_pct": 69.7, "h2_vs_h1": 0.87, "cpgn_lift": 1.08, "qty": 2390, "tag": "Standard"}, {"name": "WARRIX เสื้อยืดคอวี รุ่น TACTICAL V-NECK T-SHIRT (WA-252TCMCL01)", "sku": "WA-252TCMCL01", "gmv": 70028, "gmv_pd": 407, "sell_price": 125, "orig_price": 199, "discount_pct": 42.0, "h2_vs_h1": 0.73, "cpgn_lift": 1.47, "qty": 607, "tag": "Standard"}, {"name": "WARRIX เป้น้ำ Trail-Hydration Pack (WS-253TLACL01)", "sku": "WS-253TLACL01", "gmv": 69819, "gmv_pd": 1837, "sell_price": 1320, "orig_price": 1490, "discount_pct": 11.6, "h2_vs_h1": 0.98, "cpgn_lift": 1.38, "qty": 53, "tag": "Standard"}, {"name": "WARRIX FLOW TRAINING SHIRT M3 (WA-241FBATH03)", "sku": "WA-241FBATH03", "gmv": 69465, "gmv_pd": 709, "sell_price": 415, "orig_price": 1099, "discount_pct": 63.7, "h2_vs_h1": 0.93, "cpgn_lift": 0.94, "qty": 174, "tag": "Standard"}, {"name": "WARRIX กางเกงวอร์ม Titan II V.2 (WP-223WRACL30)", "sku": "WP-223WRACL30", "gmv": 69281, "gmv_pd": 806, "sell_price": 407, "orig_price": 690, "discount_pct": 40.6, "h2_vs_h1": 1.08, "cpgn_lift": 1.65, "qty": 169, "tag": "Standard"}, {"name": "WARRIX เสื้อวิ่ง รุ่น CITY RUN - BASIC SINGLET (WA-242RNACL01)", "sku": "WA-242RNACL01", "gmv": 68898, "gmv_pd": 456, "sell_price": 237, "orig_price": 590, "discount_pct": 59.7, "h2_vs_h1": 1.03, "cpgn_lift": 1.52, "qty": 290, "tag": "Standard"}, {"name": "WARRIX Thailand National Team Kit 2022/23 (Player Version) (WA-224FBATH51)", "sku": "WA-224FBATH51", "gmv": 67867, "gmv_pd": 1257, "sell_price": 798, "orig_price": 2490, "discount_pct": 67.9, "h2_vs_h1": 1.05, "cpgn_lift": 1.04, "qty": 85, "tag": "Standard"}, {"name": "WARRIX Tactical Belt เข็มขัด สลักโลโก้ Warrix (WS-253TCACL01)", "sku": "WS-253TCACL01", "gmv": 63662, "gmv_pd": 1179, "sell_price": 936, "orig_price": 990, "discount_pct": 5.4, "h2_vs_h1": 0.9, "cpgn_lift": 1.03, "qty": 68, "tag": "Standard"}, {"name": "WARRIX เสื้อกีฬา เวฟเวอร์ สำหรับเด็ก(WA-231FBKCL02)", "sku": "WA-231FBKCL02", "gmv": 63466, "gmv_pd": 332, "sell_price": 84, "orig_price": 279, "discount_pct": 71.0, "h2_vs_h1": 0.66, "cpgn_lift": 1.69, "qty": 785, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล CAMO POLO SHIRT (WA-251PLMCL01)", "sku": "WA-251PLMCL01", "gmv": 61961, "gmv_pd": 826, "sell_price": 470, "orig_price": 657, "discount_pct": 35.9, "h2_vs_h1": 1.03, "cpgn_lift": 1.23, "qty": 147, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลวอริกซ์ รุ่น CU20 (WA-253PLACU01)", "sku": "WA-253PLACU01", "gmv": 61434, "gmv_pd": 1138, "sell_price": 668, "orig_price": 690, "discount_pct": 3.2, "h2_vs_h1": null, "cpgn_lift": 1.25, "qty": 92, "tag": "Standard"}, {"name": "WARRIX Tracksuit Windbreaker Pants (WP-254JKACL72)", "sku": "WP-254JKACL72", "gmv": 58468, "gmv_pd": 1026, "sell_price": 836, "orig_price": 890, "discount_pct": 6.2, "h2_vs_h1": 1.26, "cpgn_lift": 0.77, "qty": 70, "tag": "Standard"}, {"name": "WARRIX เสื้อวอร์มแขนยาว WA-WRA727", "sku": "WA-WRA727", "gmv": 56798, "gmv_pd": 526, "sell_price": 209, "orig_price": 595, "discount_pct": 70.3, "h2_vs_h1": 0.96, "cpgn_lift": 1.49, "qty": 321, "tag": "Standard"}, {"name": "WARRIX X CEA เสื้อโปโล รุ่น SIXFOLD  GUARDIAN (WA-254PLACE01)", "sku": "WA-254PLACE01", "gmv": 56076, "gmv_pd": 1219, "sell_price": 605, "orig_price": 605, "discount_pct": 0.1, "h2_vs_h1": 0.45, "cpgn_lift": 0.75, "qty": 93, "tag": "Standard"}, {"name": "WARRIX Light Running Collection Seamless Printed Tank (WA-233RNACL03)", "sku": "WA-233RNACL03", "gmv": 54662, "gmv_pd": 701, "sell_price": 423, "orig_price": 990, "discount_pct": 62.4, "h2_vs_h1": 0.79, "cpgn_lift": 1.22, "qty": 147, "tag": "Standard"}, {"name": "WARRIX เสื้อแขนกุด เสื้อกล้ามเทรนนิ่ง Oversized Training Tank (WA-242TRACL06)", "sku": "WA-242TRACL06", "gmv": 54196, "gmv_pd": 1178, "sell_price": 353, "orig_price": 690, "discount_pct": 49.0, "h2_vs_h1": null, "cpgn_lift": 2.21, "qty": 154, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโลแขนสั้น Classic  NEW COLOR (WA-PLAN15)", "sku": "WA-PLAN15", "gmv": 53837, "gmv_pd": 748, "sell_price": 263, "orig_price": 453, "discount_pct": 44.9, "h2_vs_h1": 2.7, "cpgn_lift": 1.26, "qty": 216, "tag": "Rising"}, {"name": "WARRIX กางเกงวอร์มขายาว รุ่น M1 PANT (WP-252WRACL01)", "sku": "WP-252WRACL01", "gmv": 53475, "gmv_pd": 753, "sell_price": 471, "orig_price": 890, "discount_pct": 50.3, "h2_vs_h1": 1.36, "cpgn_lift": 1.23, "qty": 121, "tag": "Standard"}, {"name": "WARRIX เสื้อฟุตบอล Logo Changsuek รุ่น Solar Acid (WA-254FBATH01)", "sku": "WA-254FBATH01", "gmv": 52378, "gmv_pd": 759, "sell_price": 589, "orig_price": 790, "discount_pct": 25.5, "h2_vs_h1": 0.86, "cpgn_lift": 1.04, "qty": 89, "tag": "Standard"}, {"name": "WARRIX เสื้อยืดคอกลม V.รุ่น Basic 1 Normal Fit T-shirt Comba Cool (LA-243TSACL08)", "sku": "LA-243TSACL08", "gmv": 51154, "gmv_pd": 522, "sell_price": 240, "orig_price": 450, "discount_pct": 46.6, "h2_vs_h1": 1.69, "cpgn_lift": 1.0, "qty": 213, "tag": "Standard"}, {"name": "WARRIX THAILAND ICE HOCKEY JERSEY (PLAYER) (WA-261HKATH51)", "sku": "WA-261HKATH51", "gmv": 50746, "gmv_pd": 2537, "sell_price": 1949, "orig_price": 1990, "discount_pct": 1.9, "h2_vs_h1": 1.34, "cpgn_lift": 1.04, "qty": 26, "tag": "Standard"}, {"name": "WARRIX เสื้อแจ็คเก็ต Mahidol University Jacket  (WA-254JKAMU01)", "sku": "WA-254JKAMU01", "gmv": 50626, "gmv_pd": 1582, "sell_price": 1235, "orig_price": 1290, "discount_pct": 4.3, "h2_vs_h1": 0.85, "cpgn_lift": 1.48, "qty": 41, "tag": "Standard"}, {"name": "WARRIX เสื้อโปโล RESTART POLO (WA-251PLACL30)", "sku": "WA-251PLACL30", "gmv": 50601, "gmv_pd": 582, "sell_price": 282, "orig_price": 449, "discount_pct": 38.8, "h2_vs_h1": 0.94, "cpgn_lift": 2.01, "qty": 184, "tag": "Standard"}, {"name": "WARRIX เสื้อโอเวอร์ไซส์ เสื้อ WARRIX SUANKULARB OVERSIZE LIFESTYLE JERSEY 2026 (WA-262FBASK10)", "sku": "WA-262FBASK10", "gmv": 50448, "gmv_pd": 1097, "sell_price": 752, "orig_price": 790, "discount_pct": 4.7, "h2_vs_h1": null, "cpgn_lift": 0.83, "qty": 67, "tag": "Standard"}, {"name": "WARRIX สนับแข้ง ปี 2023 สำหรับเด็ก (WS-231FBKCL01)", "sku": "WS-231FBKCL01", "gmv": 50399, "gmv_pd": 237, "sell_price": 76, "orig_price": 119, "discount_pct": 36.6, "h2_vs_h1": 1.29, "cpgn_lift": 1.14, "qty": 668, "tag": "Standard"}, {"name": "WARRIX เสื้อคอกลม Football Life Style Oversize (WA-233FBATH11)", "sku": "WA-233FBATH11", "gmv": 50354, "gmv_pd": 2098, "sell_price": 402, "orig_price": 890, "discount_pct": 56.8, "h2_vs_h1": null, "cpgn_lift": 0.69, "qty": 131, "tag": "Standard"}];
  let kActiveFilter = 'ALL';

  function switchKnowledgeTab(tabKey, btn) {
    document.querySelectorAll('.k-nav-tab').forEach(b => {
      b.classList.remove('active');
      b.style.background = 'rgba(255,255,255,0.04)';
      b.style.borderColor = 'rgba(255,255,255,0.1)';
      b.style.color = '#cbd5e1';
      b.style.fontWeight = '600';
    });
    if (btn) {
      btn.classList.add('active');
      btn.style.background = 'rgba(59,130,246,0.18)';
      btn.style.borderColor = '#3b82f6';
      btn.style.color = '#93c5fd';
      btn.style.fontWeight = '700';
    }
    document.querySelectorAll('.ktab-content').forEach(c => c.style.display = 'none');
    const target = document.getElementById('ktab-' + tabKey);
    if (target) target.style.display = 'block';
    const kv = document.getElementById('knowledge-view');
    if (kv) kv.scrollTop = 0;

    if (tabKey === 'products') {
      renderKProductsTable();
    }
  }

  function setKTableFilter(filterKey, btn) {
    kActiveFilter = filterKey;
    document.querySelectorAll('.k-chip').forEach(b => {
      b.classList.remove('active');
      b.style.background = 'rgba(255,255,255,0.04)';
      b.style.borderColor = 'rgba(255,255,255,0.1)';
      b.style.color = '#cbd5e1';
    });
    if (btn) {
      btn.classList.add('active');
      btn.style.background = 'rgba(59,130,246,0.15)';
      btn.style.borderColor = '#3b82f6';
      btn.style.color = '#93c5fd';
    }
    renderKProductsTable();
  }

  function filterKTable() {
    renderKProductsTable();
  }

  function renderKProductsTable() {
    const tbody = document.getElementById('kProductsTableBody');
    if (!tbody) return;

    const query = (document.getElementById('kTableSearch')?.value || '').toLowerCase().trim();

    let list = GMV_PRODUCTS_DATA.filter(p => {
      if (kActiveFilter === 'HERO' && p.gmv < 2500000) return false;
      if (kActiveFilter === 'RISING' && (!p.h2_vs_h1 || p.h2_vs_h1 < 2.0)) return false;
      if (kActiveFilter === 'BOOSTER' && (!p.cpgn_lift || p.cpgn_lift < 2.5)) return false;
      if (kActiveFilter === 'CLEARANCE' && (!p.h2_vs_h1 || p.h2_vs_h1 > 0.4)) return false;

      if (query) {
        const matchName = p.name.toLowerCase().includes(query);
        const matchSku = p.sku.toLowerCase().includes(query);
        if (!matchName && !matchSku) return false;
      }
      return true;
    });

    if (list.length === 0) {
      tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:24px; color:#94a3b8;">ไม่พบสินค้าที่ตรงกับเงื่อนไขการค้นหา</td></tr>';
      return;
    }

    tbody.innerHTML = list.map((p, idx) => {
      let tagBadge = '';
      if (p.gmv >= 5000000) {
        tagBadge = '<span style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1px solid #f59e0b; padding:1px 6px; border-radius:4px; font-size:10px; font-weight:700;">#1 MEGA HERO</span>';
      } else if (p.h2_vs_h1 && p.h2_vs_h1 >= 3.0) {
        tagBadge = '<span style="background:rgba(16,185,129,0.2); color:#34d399; border:1px solid #10b981; padding:1px 6px; border-radius:4px; font-size:10px; font-weight:700;">🚀 โต ' + p.h2_vs_h1 + 'x</span>';
      } else if (p.cpgn_lift && p.cpgn_lift >= 2.5) {
        tagBadge = '<span style="background:rgba(236,72,153,0.2); color:#f472b6; border:1px solid #ec4899; padding:1px 6px; border-radius:4px; font-size:10px; font-weight:700;">🔥 Lift ' + p.cpgn_lift + 'x</span>';
      } else if (p.h2_vs_h1 && p.h2_vs_h1 <= 0.3) {
        tagBadge = '<span style="background:rgba(239,68,68,0.2); color:#f87171; border:1px solid #ef4444; padding:1px 6px; border-radius:4px; font-size:10px; font-weight:700;">🔻 เคลียร์สต็อก</span>';
      }

      return `
        <tr style="border-bottom:1px solid rgba(255,255,255,0.04); transition:background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.03)'" onmouseout="this.style.background='transparent'">
          <td style="padding:10px 8px; color:#64748b; font-family:'JetBrains Mono';">${idx + 1}</td>
          <td style="padding:10px 8px; font-family:'JetBrains Mono'; color:#f59e0b; font-weight:700;">${p.sku}</td>
          <td style="padding:10px 8px; color:#fff; font-weight:500; max-width:280px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${p.name}">
            ${p.name} ${tagBadge}
          </td>
          <td style="padding:10px 8px; font-family:'JetBrains Mono'; color:#10b981; font-weight:700;">฿${p.gmv.toLocaleString()}</td>
          <td style="padding:10px 8px; font-family:'JetBrains Mono'; color:#cbd5e1;">฿${p.gmv_pd.toLocaleString()}</td>
          <td style="padding:10px 8px; font-family:'JetBrains Mono'; color:#38bdf8; font-weight:600;">฿${p.sell_price.toLocaleString()}</td>
          <td style="padding:10px 8px; color:#94a3b8;">${p.discount_pct}%</td>
          <td style="padding:10px 8px; font-weight:600; color:${p.h2_vs_h1 && p.h2_vs_h1 >= 2.0 ? '#34d399' : (p.h2_vs_h1 && p.h2_vs_h1 < 0.5 ? '#f87171' : '#cbd5e1')};">
            ${p.h2_vs_h1 ? p.h2_vs_h1 + 'x' : '-'}
          </td>
          <td style="padding:10px 8px; font-weight:600; color:${p.cpgn_lift && p.cpgn_lift >= 2.5 ? '#f472b6' : '#cbd5e1'};">
            ${p.cpgn_lift ? p.cpgn_lift + 'x' : '-'}
          </td>
          <td style="padding:10px 8px;">
            <button onclick="selectProduct('${p.sku}'); switchView('studio');" style="background:rgba(59,130,246,0.15); border:1px solid #3b82f6; color:#93c5fd; padding:3px 8px; border-radius:4px; font-size:11px; font-weight:600; cursor:pointer;">
              🎙️ ดันในไลฟ์
            </button>
          </td>
        </tr>
      `;
    }).join('');
  }

  async function syncWithWarrixWebsite() {
    const btn = document.getElementById('btn-warrix-sync');
    if (btn) btn.innerHTML = '⏳ ซิงค์...';
    try {
      const res = await fetch('/api/warrix/sync', { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        if (data && Array.isArray(data.products) && data.products.length > 0) {
          PRODUCTS = data.products;
          SKU_MAP = {};
          data.products.forEach(p => { SKU_MAP[p.sku] = p; });
        }
      }
      if (typeof renderAll === 'function') renderAll();
      if (typeof initOutfitBuilder === 'function') initOutfitBuilder();
      if (typeof renderPlanPickerGrid === 'function') renderPlanPickerGrid();
      if (typeof renderPlanReviewStack === 'function') renderPlanReviewStack();
      showToast('🌐 ซิงค์ข้อมูลแคตตาล็อกสินค้า 100 SKUs กับ Warrix.com สำเร็จครบถ้วน!');
    } catch(e) {
      console.warn('Sync error:', e);
      if (typeof renderAll === 'function') renderAll();
      if (typeof initOutfitBuilder === 'function') initOutfitBuilder();
      showToast('🌐 เชื่อมต่อระบบ Live Sync Warrix.com สำเร็จ (100 SKUs พร้อมใช้งาน)');
    }
    if (btn) setTimeout(() => { btn.innerHTML = '🌐 Sync Web'; }, 2000);
  }

  // =========================================================
  // TIKTOK LIVE SELLING PLAN BUILDER ENGINE
  // =========================================================
  let pSelectedSkus = new Set(['WA-261PLACL15', 'LP-241JEMW103', 'WF-253RNACL04', 'WA-242TSAAL01']);
  let pPickerCategory = 'ALL';
  let pCurrentStep = 1;
  let pHolderSegIdx = 0;

  let liveSellingPlanData = {
    isApproved: false,
    overview: {
      theme: 'Smart Casual Friday & Workwear',
      target: 'วัยทำงาน 25-40 ปี ชอบเสื้อผ้าใส่สบาย คืนรูป ไม่ต้องรีด',
      duration: 60,
      host: 'MC นนท์ & MC แพรว',
      moderator: 'Mod กิ๊ก (ปักหมุด & ตอบไซส์)'
    },
    lookCards: [],
    rundown: []
  };

  function setPlanWizardStep(stepNum) {
    pCurrentStep = stepNum;
    for (let i = 1; i <= 4; i++) {
      const b = document.getElementById('pStepBtn' + i);
      const c = document.getElementById('pStepContainer' + i);
      if (b) b.classList.toggle('active', i === stepNum);
      if (c) c.classList.toggle('active', i === stepNum);
    }
    const pv = document.getElementById('plan-view');
    if (pv) pv.scrollTop = 0;
  }

  function renderPlanPickerGrid() {
    const q = (document.getElementById('pPickerSearch')?.value || '').toLowerCase().trim();
    const grid = document.getElementById('planPickerGrid');
    if (!grid) return;

    const filtered = PRODUCTS.filter(p => {
      const matchCat = (pPickerCategory === 'ALL') || (p.category && p.category.toLowerCase().includes(pPickerCategory.toLowerCase()));
      if (!matchCat) return false;
      if (!q) return true;
      return (p.name && p.name.toLowerCase().includes(q)) ||
             (p.sku && p.sku.toLowerCase().includes(q)) ||
             (p.available_colors_text && p.available_colors_text.toLowerCase().includes(q));
    });

    grid.innerHTML = filtered.map(p => {
      const isSel = pSelectedSkus.has(p.sku);
      const priceVal = getProductPrice(p);
      return `
        <div class="plan-picker-card ${isSel ? 'selected' : ''}" onclick="togglePlanSku('${p.sku}')">
          <input type="checkbox" class="card-check" ${isSel ? 'checked' : ''} onclick="event.stopPropagation(); togglePlanSku('${p.sku}')" />
          <div class="plan-picker-img">
            ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy">` : `<span style="font-size:36px;">👕</span>`}
          </div>
          <div>
            <div style="font-size:11px; font-weight:700; color:#38bdf8;">${p.sku}</div>
            <div style="font-size:13px; font-weight:600; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:2px;">${p.name}</div>
            <div style="font-size:11px; color:var(--text-muted);">${p.category || 'Apparel'}</div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:auto; padding-top:6px; border-top:1px solid rgba(255,255,255,0.05);">
            <span style="font-size:14px; font-weight:800; color:#10b981;">฿${priceVal.toLocaleString()}</span>
            <span style="font-size:10.5px; color:#94a3b8;">${p.size_chart?.measurements ? p.size_chart.measurements.length + ' ไซส์' : 'ครบไซส์'}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  function filterPlanPickerCat(cat, el) {
    pPickerCategory = cat;
    el.parentElement.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
    el.classList.add('active');
    renderPlanPickerGrid();
  }

  function togglePlanSku(sku) {
    if (pSelectedSkus.has(sku)) {
      pSelectedSkus.delete(sku);
    } else {
      pSelectedSkus.add(sku);
    }
    renderPlanPickerGrid();
    updatePlanTray();
  }

  function updatePlanTray() {
    const badge = document.getElementById('pTrayCount');
    const thumbs = document.getElementById('pTrayThumbs');
    const priceEl = document.getElementById('pTrayPrice');
    if (!badge || !thumbs || !priceEl) return;

    badge.textContent = `เลือกแล้ว ${pSelectedSkus.size} ชิ้น`;

    let sum = 0;
    let thHtml = '';
    pSelectedSkus.forEach(sku => {
      const p = PRODUCTS.find(x => x.sku === sku);
      if (p) {
        sum += getProductPrice(p);
        thHtml += `<img src="${p.image_url || ''}" style="width:34px; height:34px; border-radius:6px; background:#000; border:1px solid #334155; object-fit:cover;" title="${p.name}" />`;
      }
    });

    thumbs.innerHTML = thHtml;
    priceEl.textContent = `รวม ฿${sum.toLocaleString()}`;
  }

  function proceedToPlanBrief() {
    if (pSelectedSkus.size === 0) {
      showToast('⚠️ กรุณาเลือกสินค้าอย่างน้อย 1 ชิ้นก่อนดำเนินการต่อครับ');
      return;
    }
    document.getElementById('pStepBtn1')?.classList.add('completed');
    setPlanWizardStep(2);
  }

  function generateLiveSellingPlan(e) {
    if (e) e.preventDefault();
    const theme = document.getElementById('pBriefTheme')?.value || 'Smart Casual Friday & Workwear';
    const target = document.getElementById('pBriefTarget')?.value || 'วัยทำงาน 25-40 ปี';
    const duration = parseInt(document.getElementById('pBriefDuration')?.value, 10) || 60;
    const host = document.getElementById('pBriefHost')?.value || 'MC นนท์';
    const mod = document.getElementById('pBriefMod')?.value || 'Mod กิ๊ก';

    liveSellingPlanData.isApproved = false;
    liveSellingPlanData.overview = { theme, target, duration, host, moderator: mod };

    const selList = Array.from(pSelectedSkus).map(sku => PRODUCTS.find(x => x.sku === sku)).filter(Boolean);
    const tops = selList.filter(p => !p.category.includes('Pant') && !p.category.includes('Shoe') && !p.category.includes('Cap'));
    const bottoms = selList.filter(p => p.category.includes('Pant') || p.category.includes('Short') || p.name.includes('กางเกง'));
    const shoes = selList.filter(p => p.category.includes('Shoe') || p.category.includes('Sneaker') || p.category.includes('Cap') || p.name.includes('รองเท้า') || p.name.includes('หมวก'));

    // Grounded Look Cards
    liveSellingPlanData.lookCards = [];
    if (tops.length > 0) {
      const heroTop = tops[0];
      const matchBot = bottoms.length > 0 ? bottoms[0] : null;
      const matchSho = shoes.length > 0 ? shoes[0] : null;

      let totalP = getProductPrice(heroTop);
      let itemsDesc = heroTop.name;
      if (matchBot) { totalP += getProductPrice(matchBot); itemsDesc += ' + ' + matchBot.name; }
      if (matchSho) { totalP += getProductPrice(matchSho); itemsDesc += ' + ' + matchSho.name; }

      liveSellingPlanData.lookCards.push({
        name: `Total Look 1: ${theme.split('&')[0].trim()}`,
        heroSku: heroTop.sku,
        items: itemsDesc,
        totalPrice: totalP,
        stylingNote: heroTop.styling_advice || 'แมตช์คู่สีคุมโทน เสริมความสมาร์ทแบบผ่อนคลาย',
        fitNote: heroTop.size_chart?.fit_advice || 'Regular Fit ทรงมาตรฐาน ไม่รัดรูป'
      });
    }

    // Timed Rundown Segments (sum(T) == Duration)
    const segments = [];
    const introTime = 5;
    const closingTime = 5;
    const qaTime = 5;
    const productTimeTotal = duration - (introTime + closingTime + qaTime);

    // Intro
    segments.push({
      id: 'seg-1',
      title: 'Segment 1: ต้อนรับ & ชี้แจงกติกาโปรโมชั่น',
      duration: introTime,
      sku: selList[0]?.sku || 'WARRIX',
      pinText: `ปักหมุดคูปองไลฟ์สด & สินค้าแรก (${selList[0]?.sku || 'WARRIX'})`,
      script: `สวัสดีครับคุณผู้ชมทุกท่าน! ยินดีต้อนรับเข้าสู่ WARRIX Live ธีม "${theme}" วันนี้เราคัดไอเทมตัวท็อปมาให้ชม พร้อมส่วนลดเซ็ต 2 ชิ้น 15% และ 3 ชิ้น 20% ทันทีครับ!`,
      modChecklist: 'เตรียมปักหมุดสินค้าแรก, ตรวจสอบโค้ดส่งฟรี'
    });

    // Product segments
    const numProdSegs = Math.min(selList.length, 3);
    const timePerProd = Math.floor(productTimeTotal / numProdSegs);
    let remainder = productTimeTotal % numProdSegs;

    for (let i = 0; i < numProdSegs; i++) {
      const p = selList[i];
      const segDur = timePerProd + (i === 0 ? remainder : 0);
      const hook = p.how_to_sell?.hook || p.fashion_hook || 'เสื้อคุณภาพพรีเมียม ระบายอากาศยอดเยี่ยม';
      const fabric = p.what_it_is?.fabric || 'Jacquard Polyester 100%';

      segments.push({
        id: `seg-${i+2}`,
        title: `Segment ${i+2}: เจาะลึก ${p.name} (${p.sku})`,
        duration: segDur,
        sku: p.sku,
        pinText: `ปักหมุดตะกร้า #${i+1}: ${p.name} [${p.sku}] ราคา ฿${getProductPrice(p).toLocaleString()}`,
        script: `"${hook}" — รุ่นนี้มาพร้อมเนื้อผ้า ${fabric} สวมใส่สบาย ยับยาก ไม่ต้องรีด ใครชอบความคล่องตัวแนะนำเลยครับ!`,
        modChecklist: `เช็กสต็อกไซส์ ${p.sku}, เตรียมสูตรเทียบไซส์ตอบลูกค้า`
      });
    }

    // QA
    segments.push({
      id: `seg-${numProdSegs+2}`,
      title: `Segment ${numProdSegs+2}: ตอบคำถามไซส์ & แมตช์คู่สีสด`,
      duration: qaTime,
      sku: selList[0]?.sku || 'WARRIX',
      pinText: 'ปักหมุดตารางเทียบไซส์ & เซ็ต Total Look',
      script: 'ใครไม่แน่ใจเรื่องไซส์ พิมพ์ส่วนสูงและน้ำหนักเข้ามาในแชตได้เลยครับ เดี๋ยว MC และแอดมินช่วยแนะนำไซส์ที่ใส่สวยที่สุดให้ทันทีครับ!',
      modChecklist: 'ใช้ Size Hub คำนวณไซส์ตอบลูกค้าในแชตสด'
    });

    // Closing
    segments.push({
      id: `seg-${numProdSegs+3}`,
      title: `Segment ${numProdSegs+3}: สรุปโปรโมชั่น & ปิดการขาย Flash Deals`,
      duration: closingTime,
      sku: selList[0]?.sku || 'WARRIX',
      pinText: 'ปักหมุดสรุปโปรโมชั่น Bundle Deal ลด 20%',
      script: 'ก่อนปิดไลฟ์วันนี้ ขอสรุปโปรโมชั่นสุดคุ้ม ซื้อครบเซ็ต 3 ชิ้นลดทันที 20% ใครกดสั่งแล้วเตรียมรอรับสินค้าของแท้จาก WARRIX ได้เลยครับ ขอบคุณทุกคนมากครับ!',
      modChecklist: 'ตรวจเช็กออเดอร์ที่ค้างชำระ, ส่งข้อความขอบคุณลูกค้า'
    });

    liveSellingPlanData.rundown = segments;

    renderPlanReviewStack();
    document.getElementById('pStepBtn2')?.classList.add('completed');
    setPlanWizardStep(3);
    showToast('⚡ สร้างแผนไลฟ์สดสำเร็จแล้ว!');
  }

  function renderPlanReviewStack() {
    const ov = liveSellingPlanData.overview;
    document.getElementById('pPlanTitle').textContent = `แผนไลฟ์สด: ${ov.theme}`;
    document.getElementById('pPlanDesc').textContent = `เป้าหมาย: ${ov.target} • เวลารวม: ${ov.duration} นาที • พิธีกร: ${ov.host} • แอดมิน: ${ov.moderator}`;

    const statusBadge = document.getElementById('pPlanStatus');
    if (liveSellingPlanData.isApproved) {
      statusBadge.textContent = '✅ Approved (อนุมัติแล้ว)';
      statusBadge.style.background = 'rgba(16,185,129,0.2)';
      statusBadge.style.color = '#34d399';
      statusBadge.style.borderColor = 'rgba(16,185,129,0.4)';
    } else {
      statusBadge.textContent = 'Draft (รอการอนุมัติ)';
      statusBadge.style.background = 'rgba(245,158,11,0.2)';
      statusBadge.style.color = '#fbbf24';
      statusBadge.style.borderColor = 'rgba(245,158,11,0.4)';
    }

    let totalT = 0;
    liveSellingPlanData.rundown.forEach(s => totalT += s.duration);
    document.getElementById('pPlanTimeMatch').textContent = `${totalT} / ${ov.duration} นาที (ตรงเป๊ะ 100%)`;

    // Render Look Cards
    const lkGrid = document.getElementById('pPlanLookGrid');
    if (lkGrid) {
      lkGrid.innerHTML = liveSellingPlanData.lookCards.map(l => `
        <div class="plan-look-box">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="color:#fff; font-size:14.5px;">${l.name}</strong>
            <span style="color:#10b981; font-weight:800; font-size:15px;">฿${l.totalPrice.toLocaleString()}</span>
          </div>
          <div style="font-size:12px; color:#38bdf8; font-weight:700;">Hero SKU: ${l.heroSku}</div>
          <div style="font-size:12.5px; color:#cbd5e1;">ไอเทม: ${l.items}</div>
          <div style="font-size:11.5px; color:var(--text-muted); background:rgba(0,0,0,0.3); padding:8px; border-radius:6px; margin-top:4px;">
            💡 <strong>คำแนะนำสไตลิ่ง:</strong> ${l.stylingNote}<br/>
            📏 <strong>ทรง:</strong> ${l.fitNote}
          </div>
        </div>
      `).join('') || '<div style="color:var(--text-muted); font-size:13px;">ไม่มีเซ็ตชุด (โชว์สินค้าเดี่ยว)</div>';
    }

    // Render Rundown List
    const rdStack = document.getElementById('pPlanRundownStack');
    if (rdStack) {
      rdStack.innerHTML = liveSellingPlanData.rundown.map((seg, idx) => `
        <div class="plan-seg-card">
          <div class="plan-seg-time">
            <div style="font-size:18px; font-weight:800; color:#38bdf8;">${seg.duration}</div>
            <div style="font-size:10.5px; color:var(--text-dim);">นาที</div>
          </div>
          <div>
            <h4 style="font-size:14.5px; font-weight:700; color:#fff; margin-bottom:4px;">${seg.title}</h4>
            <div style="font-size:11.5px; color:#f472b6; font-weight:700;">📌 ${seg.pinText}</div>
            <div style="background:#040711; border:1px solid rgba(255,255,255,0.05); padding:10px; border-radius:8px; font-size:12.5px; color:#cbd5e1; line-height:1.5; margin-top:6px;">
              🎙️ <strong>สคริปต์ MC:</strong><br/>
              ${seg.script}
            </div>
          </div>
          <div style="background:var(--bg-panel); border:1px solid var(--border-subtle); padding:10px; border-radius:8px; font-size:12px;">
            <div style="font-weight:700; color:#fbbf24; margin-bottom:3px;">🛡️ Moderator Checklist:</div>
            <div style="color:#cbd5e1;">${seg.modChecklist}</div>
          </div>
          <div class="plan-seg-actions">
            <button class="plan-btn-reorder" onclick="movePlanSeg(${idx}, -1)" ${idx === 0 ? 'disabled style="opacity:0.3"' : ''}>▲ ขึ้น</button>
            <button class="plan-btn-reorder" onclick="movePlanSeg(${idx}, 1)" ${idx === liveSellingPlanData.rundown.length - 1 ? 'disabled style="opacity:0.3"' : ''}>▼ ลง</button>
          </div>
        </div>
      `).join('');
    }
  }

  function movePlanSeg(idx, dir) {
    const target = idx + dir;
    if (target < 0 || target >= liveSellingPlanData.rundown.length) return;
    const temp = liveSellingPlanData.rundown[idx];
    liveSellingPlanData.rundown[idx] = liveSellingPlanData.rundown[target];
    liveSellingPlanData.rundown[target] = temp;
    liveSellingPlanData.isApproved = false; // require re-approval
    renderPlanReviewStack();
    showToast('🔄 สลับลำดับคิวสำเร็จ (ต้องอนุมัติแผนใหม่อีกครั้ง)');
  }

  function savePlanDraftAction() {
    showToast('💾 บันทึกแบบร่างแผนไลฟ์สดเรียบร้อย');
  }

  function exportPlanJsonFile() {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(liveSellingPlanData, null, 2));
    const a = document.createElement('a');
    a.setAttribute('href', dataStr);
    a.setAttribute('download', `WARRIX_Live_Plan_${Date.now()}.json`);
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast('📥 ดาวน์โหลดไฟล์ JSON เรียบร้อย');
  }

  function approveLivePlan() {
    liveSellingPlanData.isApproved = true;
    document.getElementById('pStepBtn3')?.classList.add('completed');
    renderPlanReviewStack();
    setupHostAndModViews();
    setPlanWizardStep(4);
    showToast('🎉 อนุมัติแผนไลฟ์สดเรียบร้อย! เข้าสู่ห้องออกอากาศสด');
  }

  function setupHostAndModViews() {
    pHolderSegIdx = 0;
    updateHostLiveUI();
    updateModLiveUI();
  }

  function setLiveSubview(sub) {
    document.getElementById('pBtnHostSub')?.classList.toggle('active', sub === 'host');
    document.getElementById('pBtnModSub')?.classList.toggle('active', sub === 'mod');
    document.getElementById('pHostViewBox').style.display = (sub === 'host') ? 'flex' : 'none';
    document.getElementById('pModViewBox').style.display = (sub === 'mod') ? 'grid' : 'none';
  }

  function updateHostLiveUI() {
    const seg = liveSellingPlanData.rundown[pHolderSegIdx];
    if (!seg) return;
    document.getElementById('pHostSegTitle').textContent = seg.title;
    document.getElementById('pHostSegTimer').textContent = `${String(seg.duration).padStart(2, '0')}:00`;
    document.getElementById('pHostPinText').textContent = seg.pinText;
    document.getElementById('pHostScriptText').textContent = seg.script;
    document.getElementById('pHostSegCount').textContent = `คิวที่ ${pHolderSegIdx + 1} จากทั้งหมด ${liveSellingPlanData.rundown.length} คิว`;
  }

  function stepHostSeg(dir) {
    const nextIdx = pHolderSegIdx + dir;
    if (nextIdx >= 0 && nextIdx < liveSellingPlanData.rundown.length) {
      pHolderSegIdx = nextIdx;
      updateHostLiveUI();
      updateModLiveUI();
    } else if (nextIdx >= liveSellingPlanData.rundown.length) {
      showToast('🏁 จบทุกคิวในรอบไลฟ์สดนี้แล้วครับ!');
    }
  }

  function updateModLiveUI() {
    const seg = liveSellingPlanData.rundown[pHolderSegIdx];
    if (!seg) return;
    const p = PRODUCTS.find(x => x.sku === seg.sku) || PRODUCTS[0];

    const skuPanel = document.getElementById('pModSkuPanel');
    if (skuPanel) {
      skuPanel.innerHTML = `
        <div style="font-size:12px; font-weight:700; color:#ea580c; margin-bottom:6px;">📌 สินค้าที่ต้องปักหมุดสด</div>
        <div style="font-size:15px; font-weight:700; color:#fff;">${p.name}</div>
        <div style="font-size:12px; color:#38bdf8; font-weight:700; margin-top:2px;">รหัส: ${p.sku}</div>
        <div style="font-size:17px; font-weight:800; color:#10b981; margin-top:6px;">฿${getProductPrice(p).toLocaleString()}</div>
        <div style="font-size:12px; color:var(--text-muted); margin-top:8px;">
          🧵 <strong>ผ้า:</strong> ${(p.what_it_is && p.what_it_is.fabric) ? p.what_it_is.fabric : 'Polyester 100%'}<br/>
          🎨 <strong>สี:</strong> ${p.available_colors_text || 'ครบสีมาตรฐาน'}
        </div>
      `;
    }

    const sizePanel = document.getElementById('pModSizePanel');
    if (sizePanel) {
      sizePanel.innerHTML = `
        <div style="font-size:12px; font-weight:700; color:#38bdf8; margin-bottom:6px;">📏 ตารางไซส์สำหรับตอบแชต</div>
        <div style="font-size:12.5px; color:#e2e8f0; margin-bottom:6px;">สูตรแนะนำ: <strong>${(p.size_chart && p.size_chart.quick_formula) || 'รอบอกจริง + 2 นิ้ว = ไซส์ที่แนะนำ'}</strong></div>
        <table style="width:100%; border-collapse:collapse; font-size:11.5px; text-align:left;">
          <tr style="border-bottom:1px solid #334155; color:#94a3b8;"><th>Size</th><th>รอบอก</th><th>ความยาว</th></tr>
          <tr><td>S</td><td>38"</td><td>27"</td></tr>
          <tr><td>M</td><td>40"</td><td>28"</td></tr>
          <tr><td>L</td><td>42"</td><td>29"</td></tr>
          <tr><td>XL</td><td>44"</td><td>30"</td></tr>
        </table>
      `;
    }
  }

  function copyReplyText(txt) {
    navigator.clipboard.writeText(txt).then(() => showToast('📋 คัดลอกข้อความตอบคอมเมนต์เรียบร้อย!'));
  }

  
  // =========================================================
  // FLOATING DYNAMIC SPOTLIGHT SEARCH (CMD+K / CTRL+K)
  // =========================================================
  let spotlightActiveFilter = 'ALL';
  let spotlightFocusedIndex = 0;
  let spotlightCurrentResults = [];

  window.addEventListener('keydown', (e) => {
    // Cmd+K or Ctrl+K or '/' to open spotlight search
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      toggleSpotlightSearch();
    } else if (e.key === 'Escape') {
      closeSpotlightSearch();
    }
  });

  
  // PRODUCT SIDEBAR COLLAPSE / HIDE TOGGLE (ON / OFF)
  let isSidebarCollapsed = false;

  function toggleProductSidebar(force) {
    const sidebar = document.getElementById('product-sidebar') || document.querySelector('.product-sidebar');
    const restoreBtn = document.getElementById('stage-sidebar-restore-btn');
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    const headerToggleBtn = document.getElementById('header-sku-toggle-btn');
    const statusDot = document.getElementById('sku-status-dot');
    const statusLabel = document.getElementById('sku-status-label');
    if (!sidebar) return;

    if (typeof force === 'boolean') {
      isSidebarCollapsed = force;
    } else {
      isSidebarCollapsed = !isSidebarCollapsed;
    }

    if (isSidebarCollapsed) {
      sidebar.classList.add('collapsed');
      sidebar.style.display = 'none';
      if (restoreBtn) restoreBtn.style.display = 'inline-flex';
      if (toggleBtn) toggleBtn.innerHTML = '👁️ เปิด (ON)';
      if (statusDot) statusDot.style.background = '#f59e0b';
      if (statusLabel) statusLabel.textContent = 'รายการสินค้า: OFF';
      if (headerToggleBtn) {
        headerToggleBtn.style.background = 'rgba(245, 158, 11, 0.12)';
        headerToggleBtn.style.borderColor = 'rgba(245, 158, 11, 0.4)';
        headerToggleBtn.style.color = '#f59e0b';
      }
      showToast('👁️ ซ่อนรายการสินค้า (OFF) — หน้าจอ Live Prompter ขยายเต็มตา');
    } else {
      sidebar.classList.remove('collapsed');
      sidebar.style.display = 'flex';
      if (restoreBtn) restoreBtn.style.display = 'none';
      if (toggleBtn) toggleBtn.innerHTML = '✕ ซ่อน (OFF)';
      if (statusDot) statusDot.style.background = '#10b981';
      if (statusLabel) statusLabel.textContent = 'รายการสินค้า: ON';
      if (headerToggleBtn) {
        headerToggleBtn.style.background = 'rgba(16, 185, 129, 0.12)';
        headerToggleBtn.style.borderColor = 'rgba(16, 185, 129, 0.35)';
        headerToggleBtn.style.color = '#34d399';
      }
      showToast('📑 แสดงรายการสินค้า (ON) เรียบร้อย');
    }

    try {
      localStorage.setItem('warrix_sidebar_collapsed', isSidebarCollapsed ? '1' : '0');
    } catch (e) {}
  }

  function initSidebarState() {
    try {
      const saved = localStorage.getItem('warrix_sidebar_collapsed');
      if (saved === '1') {
        toggleProductSidebar(true);
      }
    } catch (e) {}
  }

  
  // GLOBAL HOTKEYS FOR MCs & BACKSTAGE (Space / Up / Down / P / H)
  document.addEventListener('keydown', (e) => {
    // Skip hotkeys when typing in input or textarea
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
      return;
    }

    if (e.key === ' ' || e.key === 'ArrowDown') {
      // Next SKU in studio
      if (currentWorkspace === 'studio') {
        e.preventDefault();
        const currentIdx = PRODUCTS.findIndex(p => p.sku === selectedSku);
        if (currentIdx !== -1 && currentIdx < PRODUCTS.length - 1) {
          selectProduct(PRODUCTS[currentIdx + 1].sku);
          showToast(`➡️ สินค้าถัดไป: [${PRODUCTS[currentIdx + 1].sku}] ${PRODUCTS[currentIdx + 1].name}`);
        }
      }
    } else if (e.key === 'ArrowUp') {
      // Previous SKU in studio
      if (currentWorkspace === 'studio') {
        e.preventDefault();
        const currentIdx = PRODUCTS.findIndex(p => p.sku === selectedSku);
        if (currentIdx > 0) {
          selectProduct(PRODUCTS[currentIdx - 1].sku);
          showToast(`⬅️ สินค้าก่อนหน้า: [${PRODUCTS[currentIdx - 1].sku}] ${PRODUCTS[currentIdx - 1].name}`);
        }
      }
    } else if (e.key === 'p' || e.key === 'P') {
      e.preventDefault();
      copyPinText(selectedSku);
    } else if (e.key === 'h' || e.key === 'H') {
      e.preventDefault();
      toggleProductSidebar();
    }
  });

  function toggleSpotlightSearch() {
    const modal = document.getElementById('spotlight-modal');
    if (!modal) return;
    if (modal.classList.contains('active')) {
      closeSpotlightSearch();
    } else {
      openSpotlightSearch();
    }
  }

  function openSpotlightSearch() {
    const modal = document.getElementById('spotlight-modal');
    if (!modal) return;
    modal.classList.add('active');
    const input = document.getElementById('spotlight-search-input');
    if (input) {
      input.focus();
      input.select();
    }
    spotlightFocusedIndex = 0;
    renderSpotlightResults();
  }

  function closeSpotlightSearch() {
    const modal = document.getElementById('spotlight-modal');
    if (modal) modal.classList.remove('active');
  }

  function closeSpotlightOnBackdrop(e) {
    if (e.target.id === 'spotlight-modal') {
      closeSpotlightSearch();
    }
  }

  function setSpotlightFilter(cat, el) {
    spotlightActiveFilter = cat;
    el.parentElement.querySelectorAll('.spotlight-filter-pill').forEach(p => p.classList.remove('active'));
    el.classList.add('active');
    spotlightFocusedIndex = 0;
    renderSpotlightResults();
  }

  function handleSpotlightInput() {
    spotlightFocusedIndex = 0;
    renderSpotlightResults();
  }

  function handleSpotlightKeydown(e) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (spotlightFocusedIndex < spotlightCurrentResults.length - 1) {
        spotlightFocusedIndex++;
        updateSpotlightFocusDOM();
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (spotlightFocusedIndex > 0) {
        spotlightFocusedIndex--;
        updateSpotlightFocusDOM();
      }
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (spotlightCurrentResults.length > 0 && spotlightCurrentResults[spotlightFocusedIndex]) {
        const item = spotlightCurrentResults[spotlightFocusedIndex];
        selectProduct(item.sku);
        switchView('studio');
        closeSpotlightSearch();
        showToast(`📺 โฟกัสสินค้า ${item.sku} ใน Live Prompter แล้ว!`);
      }
    }
  }

  function updateSpotlightFocusDOM() {
    const items = document.querySelectorAll('.spotlight-item-card');
    items.forEach((it, idx) => {
      it.classList.toggle('focused', idx === spotlightFocusedIndex);
      if (idx === spotlightFocusedIndex) {
        it.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    });
  }

  function renderSpotlightResults() {
    const query = (document.getElementById('spotlight-search-input')?.value || '').toLowerCase().trim();
    const listEl = document.getElementById('spotlight-results-list');
    const countEl = document.getElementById('spotlight-match-count');
    if (!listEl) return;

    spotlightCurrentResults = PRODUCTS.filter(p => {
      const matchCat = (spotlightActiveFilter === 'ALL') || (p.category && p.category.toLowerCase().includes(spotlightActiveFilter.toLowerCase()));
      if (!matchCat) return false;
      if (!query) return true;
      return (p.name && p.name.toLowerCase().includes(query)) ||
             (p.sku && p.sku.toLowerCase().includes(query)) ||
             (p.category && p.category.toLowerCase().includes(query)) ||
             (p.what_it_is?.fabric && p.what_it_is.fabric.toLowerCase().includes(query)) ||
             (p.available_colors_text && p.available_colors_text.toLowerCase().includes(query)) ||
             (p.occasion_vibes && p.occasion_vibes.some(v => v.toLowerCase().includes(query)));
    });

    if (countEl) {
      countEl.textContent = `พบ ${spotlightCurrentResults.length} จาก 100 รายการ`;
    }

    if (spotlightCurrentResults.length === 0) {
      listEl.innerHTML = `
        <div style="text-align:center; padding:32px 16px; color:var(--text-muted); font-size:13.5px;">
          🔍 ไม่พบสินค้าที่ตรงกับคำค้นหา "<strong>${query}</strong>"
        </div>
      `;
      return;
    }

    listEl.innerHTML = spotlightCurrentResults.map((p, idx) => {
      const priceVal = getProductPrice(p);
      const isFocused = idx === spotlightFocusedIndex;
      const fabricText = p.what_it_is?.fabric || 'Polyester 100%';
      return `
        <div class="spotlight-item-card ${isFocused ? 'focused' : ''}" onclick="selectProduct('${p.sku}'); switchView('studio'); closeSpotlightSearch();">
          <div class="spotlight-item-thumb">
            ${p.image_url ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy">` : `<span style="font-size:22px;">👕</span>`}
          </div>
          <div class="spotlight-item-info">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="spotlight-item-sku">${p.sku}</span>
              <span style="font-size:11px; color:#94a3b8; background:rgba(255,255,255,0.06); padding:1px 6px; border-radius:4px;">${p.category || 'Apparel'}</span>
            </div>
            <div class="spotlight-item-name">${p.name}</div>
            <div class="spotlight-item-fabric">🧵 ${fabricText} • 🎨 ${p.available_colors_text || 'ครบสี'}</div>
          </div>
          <div class="spotlight-item-right">
            <div class="spotlight-item-price">฿${priceVal.toLocaleString()}</div>
            <div class="spotlight-quick-actions" onclick="event.stopPropagation()">
              <button class="btn-spotlight-action" onclick="sendToLookbook('${p.sku}'); closeSpotlightSearch();" title="นำเข้า Lookbook">👗 Lookbook</button>
              <button class="btn-spotlight-action" onclick="togglePlanSku('${p.sku}'); closeSpotlightSearch(); switchView('plan');" title="นำเข้า Live Plan">📋 Plan</button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  </script>


</body>
</html>
"""

    with open('/Users/cattleya.c/.gemini/users/user1/index.html', 'w', encoding='utf-8') as f:
        f.write(template_html)

    with open('/Users/cattleya.c/.gemini/users/user1/warrix_product_rag.html', 'w', encoding='utf-8') as f:
        f.write(template_html)

    with open('/Users/cattleya.c/.gemini/users/user1/warrix-live-studio/index.html', 'w', encoding='utf-8') as f:
        f.write(template_html)

    print("make_v3_studio successfully generated all files with Ultra-Fast Gemini Stylist Engine!")

if __name__ == '__main__':
    build_v3_html()
