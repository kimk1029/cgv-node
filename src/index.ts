import puppeteer, { Browser, Page } from "puppeteer";
import login from "./components/login";
import { waitThreeSeconds } from "./utils/wait";
import { findMovie } from "./components/findMovie";
import { startBrowser } from "./components/init";
import { selectDayTime } from "./components/dayandtime";

const MOVIENAME = "듄-파트2";
// 메인 로직
async function main() {
  const { browser, page } = await startBrowser();

  await login(page);
  await findMovie(page, MOVIENAME);
  await selectDayTime(page, "20240330", ["2100", "2500"]);
  // 필요한 작업을 마친 후 브라우저 종료
  await browser.close();
}

main().catch(console.error);
