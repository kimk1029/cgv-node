import { Page } from "puppeteer";

const ID = "kimk1029";
const PASSWORD = "aormsja!4";
async function login(page: Page) {
  const loginUrl = "https://www.cgv.co.kr/user/login/";
  await page.goto(loginUrl, { waitUntil: "networkidle2" });

  // 로그인 과정
  await page.type("#txtUserId", ID);
  await page.type("#txtPassword", PASSWORD);
  const navigationPromise = page.waitForNavigation();
  await Promise.all([
    page.click("#submit"), // 로그인 버튼 클릭
    navigationPromise, // 다음 페이지로의 이동이 완료될 때까지 기다림
  ]);
  await page.screenshot({ path: "example1.png" });
  // 추가적인 대기 조건이 필요하다면 여기에 구현
}
export default login;
