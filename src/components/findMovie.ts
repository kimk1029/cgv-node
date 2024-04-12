import puppeteer, { Page } from "puppeteer";
import { waitThreeSeconds } from "../utils/wait";

export async function findMovie(page: Page, name: string): Promise<boolean> {
  await page.goto("http://www.cgv.co.kr/ticket/");

  // iframe으로 전환
  const frameElement = await page.waitForSelector("iframe#ticket_iframe");
  const frame = await frameElement?.contentFrame();
  let passValue = false;
  // 영화 목록 로딩 대기
  const movieListSelector =
    "div.movie-list.nano.has-scrollbar.has-scrollbar-y > ul > li";
  await frame?.waitForSelector(movieListSelector, { visible: true });
  const movieList = await frame?.$$(movieListSelector);

  if (movieList) {
    for (const movie of movieList) {
      const movieText: string | null = await (
        await movie.getProperty("textContent")
      ).jsonValue();
      if (movieText?.includes(name) && !movieText.includes("[")) {
        await movie.evaluate((movieElement) => {
          (movieElement.querySelector("a") as HTMLAnchorElement)?.click();
        });
        passValue = true;
        break;
      }
    }
  }

  if (!passValue) {
    console.log("영화를 찾을 수 없습니다.");
    return false;
  }

  // IMAX 선택
  try {
    await frame?.waitForSelector("div.checkedBD", {
      timeout: 5000,
      visible: true,
    });
    const imaxButton = await frame?.$('li#sbmt_imax > a[data-type="IMAX"]');
    await waitThreeSeconds();
    await imaxButton?.click();
    await waitThreeSeconds();
    passValue = true;
  } catch (error) {
    console.log("IMAX 옵션이 없습니다.");
    passValue = false;
  }

  if (!passValue) {
    return false;
  }

  // 극장 선택
  try {
    const theaterSelector = 'li[theater_cd="0013"]';
    await frame?.waitForSelector(theaterSelector, { timeout: 5000 });
    await frame?.click(theaterSelector);
    await waitThreeSeconds();
    await page.screenshot({ path: "2222.png" });
    passValue = true;
  } catch (error) {
    console.log("극장을 선택할 수 없습니다.");
    passValue = false;
  }

  return passValue;
}
