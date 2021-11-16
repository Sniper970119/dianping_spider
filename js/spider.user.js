// ==UserScript==
// @name         大众点评评论
// @namespace    http://tampermonkey.net/
// @version      0.10
// @description  获取大众点评网页评论,解决动态字体加密
// @author       You
// @match        http://www.dianping.com/shop*
// @match        https://www.dianping.com/shop*
// @icon         https://www.google.com/s2/favicons?domain=dianping.com
// @grant        GM.xmlHttpRequest
// ==/UserScript==
/* global html2canvas Tesseract */
 
const moreBtnClass = '.fold';
const lessBtnClass = '.unfold';
const commentClass = '.review-words';
const nextBtnClass = '.NextPage';
 
(function() {
  'use strict';
  const $ = document.querySelectorAll.bind(document);
 
  const getResult = async () => {
    const $ = document.querySelectorAll.bind(document);
    const documentTxt = new XMLSerializer().serializeToString(document);
 
    const getCssUrl = () => {
      const bar = documentTxt.matchAll(/href=\"(\/\/s3plus\.meituan\.net\/v1\/.*?)\"/g);
      const baz = [...bar];
      return baz.map(b => 'https:' + b[1]);
    }
 
    const getSvgUrl = (content) => {
      const bar = content.matchAll(/\[class\^=\"(.*?)\"\].*?url\((\/\/s3plus.meituan.net\/v1\/.*?)\)/g);
      const baz = [...bar];
      return baz;
    }
 
    const getFileViaUrl = url => {
      return new Promise((resolve, reject) => {
        GM.xmlHttpRequest({
          method: 'GET',
          url: url,
          responseType: 'text',
          headers: {
            'Content-Type': 'text/css'
          },
          onload: response => {
            if (response.status === 200) return resolve(response.response)
            else return resolve('');
          }
        });
      });
    }
 
    const cssNameMap = {};
    const svgMap = {};
    const urls = getCssUrl();
    let svgUrls = [];
    for(let i = 0;i < urls.length;i += 1) {
      const cssContent = await getFileViaUrl(urls[i]);
      const matchs = cssContent.matchAll(/.(.*?)\{background:-(.*?)px -(.*?)px;}/mg);
      const matchNames = [...matchs];
      matchNames.forEach(name => {
        if (!name[0].includes('[')) {
          cssNameMap[name[1]] = [+Number(name[2]).toFixed(0), +Number(name[3]).toFixed(0)]
        }
      });
      const svgUrl = getSvgUrl(cssContent);
      svgUrls = [...svgUrl, ...svgUrls];
    }
 
    for(let i = 0;i < svgUrls.length;i += 1) {
      const svgContent = await getFileViaUrl(svgUrls[i][2]);
      const fontLocMap = [...svgContent.matchAll(/<text x=\".*?\" y=\"(.*?)\">(.*?)<\/text>/mg)];
      let fontHeightOffset =0;
      let fontWeightOffset = 0
      if (svgContent.includes('#333')) {
        fontHeightOffset = 23;
        fontWeightOffset = 0;
      }
      if (svgContent.includes('#666')) {
        fontHeightOffset = 15;
        fontWeightOffset = 0;
      }
      const fontLoc = {};
      fontLocMap.forEach((fl, idx) => {
        fontLoc[fl[1]] = idx + 1;
      });
      svgMap[svgUrls[i][1]] = {};
      svgMap[svgUrls[i][1]]['fontLocMap'] = fontLocMap;
      svgMap[svgUrls[i][1]]['fontHeightOffset'] = fontHeightOffset;
      svgMap[svgUrls[i][1]]['fontWeightOffset'] = fontWeightOffset;
      svgMap[svgUrls[i][1]]['fontLoc'] = fontLoc;
    }
    // console.log('svgMap', svgMap);
    Object.keys(cssNameMap).forEach((key, idx) => {
      const arr = cssNameMap[key];
      const foo =key.slice(0, 3);
      const fontMap = svgMap[foo];
      if (!fontMap) return;
      const locX = arr[0];
      const locY = arr[1];
      const fontHeightOffset = fontMap.fontHeightOffset;
      const fontWeightOffset = fontMap.fontWeightOffset;
      const fontLoc = fontMap.fontLoc;
      const fontLocMap = fontMap.fontLocMap;
      const locXLine = Math.floor((locX + fontWeightOffset) / 14);
      const locYLine = fontLoc[locY + fontHeightOffset];
      let val = '';
      if (fontLocMap[locYLine - 1]) val = fontLocMap[locYLine - 1][2][locXLine];
      cssNameMap[key].push(val);
    });
    // console.log('cssMap', cssNameMap)
    const comments = [...$(commentClass)];
    const result = [];
    comments.forEach(cmt => {
      const imgs = cmt.querySelectorAll('img');
      imgs.forEach(img => cmt.removeChild(img));
      const nodes = [...cmt.childNodes];
      let foo = '';
      nodes.forEach(node => {
        const cls = node.className;
        if (cls) {
          const bar = cssNameMap[cls];
          if (bar) foo += bar[2];
        } else foo += node.textContent;
      });
      result.push(foo.trim());
    });
 
    return result;
  }
 
  const showResult = (pics) => {
    let foo = document.createElement('p');
    foo.innerHTML = pics.map(p => '<div style="margin-top: 20px;">' + p + '</div>').join(` `);
    foo.style.position = 'fixed';
    foo.style.width = '600px';
    foo.style.height = '600px';
    foo.style.left = '10px';
    foo.style.bottom = '20px';
    foo.style.padding = '20px';
    foo.style.background = '#61ffff';
    foo.style.overflow = 'auto';
    document.body.appendChild(foo);
  }
 
  let btn = document.createElement('button');
  let next = document.createElement('button');
  btn.innerHTML = '开始采集';
  btn.style.position = 'fixed'
  btn.style.right = '20px';
  btn.style.bottom = '80px';
 
  next.innerHTML = '下一页';
  next.style.position = 'fixed'
  next.style.right = '20px';
  next.style.bottom = '120px';
 
  document.body.appendChild(btn);
  document.body.appendChild(next);
 
  btn.onclick = async () => {
    const moreBtns = $(moreBtnClass);
    moreBtns.forEach(b => {
      b.click();
      b.style.opacity = 0;
    });
    const lessBtns = $(lessBtnClass);
    lessBtns.forEach(l => l.style.opacity = 0);
    const res = await getResult();
    showResult(res);
  }

  next.onclick = () => {
    const nextBtn = $(nextBtnClass)[0];
    if (nextBtn) nextBtn.click();
  }
 
})();
