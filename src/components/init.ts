import puppeteer from "puppeteer";

export async function startBrowser() {
  const browser = await puppeteer.launch({ headless: false }); // 브라우저 인스턴스 생성
  const page = await browser.newPage(); // 새 페이지 열기
  // await page.setViewport({ width: 2020, height: 1080 });
  return { browser, page };
}
