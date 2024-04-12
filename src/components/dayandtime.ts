import { ElementHandle, Frame, Page } from "puppeteer";
import { waitThreeSeconds } from "../utils/wait";

export async function selectDayTime(
  page: Page,
  day: string,
  time: string[]
): Promise<void> {
  let movieReady: boolean = false;
  const frameElement = await page.waitForSelector("iframe#ticket_iframe");
  const frame = await frameElement?.contentFrame();
  while (!movieReady) {
    const dayList: ElementHandle[] = await getOption(frame);
    const theDay = [];
    for (const yymmdd of dayList) {
      const dateAttribute: string | null = await yymmdd.evaluate((el) =>
        el.getAttribute("date")
      );
      console.log("DATE : " + dateAttribute);
      if (dateAttribute?.includes(day)) {
        theDay.push(yymmdd);
      }
    }

    await delayClick(theDay[0], "날짜");
    if (frame) {
      let list = await frame.$$("div.theater > ul > li");

      while (list.length < 1) {
        list = await frame.$$("div.theater > ul > li");
      }
      for (const theTime of list) {
        const playStartTime: string | null = await theTime.evaluate((el) =>
          el.getAttribute("play_start_tm")
        );
        const countText: string = await theTime.$eval(
          "a > span.count",
          (element) => element.textContent || ""
        );
        if (
          playStartTime &&
          isTimeInRange(playStartTime, [time[0], time[1]]) &&
          countText !== "준비중"
        ) {
          console.log("시작시간 찾음> >", playStartTime);
          console.log(theTime);
          movieReady = true;
          await waitThreeSeconds();
          await delayClick(theTime, "시간");
          break;
        }
      }
    }
  }
  await waitThreeSeconds();
  const select = await frame?.$("a.btn-right.on");
  if (select) {
    console.log("SELECT:::", select);
    await delayClick(select, "좌석선택");
  }
}

async function delayClick(
  element: ElementHandle<Element> | null,
  comment: string
): Promise<void> {
  console.log(`[${comment}]`);
  if (!element) {
    console.log("Element is null");
    return;
  }

  for (let i = 1; i <= 20; i++) {
    try {
      await element.click();
      console.log(`${comment} 선택`);
      break; // 클릭에 성공하면 반복문을 종료합니다.
    } catch (error: Error | any) {
      console.log(`${i}번째 ${comment} 선택 실패: `, error.message);
      // 실패한 경우에는 약간의 지연 후 다시 시도합니다.
      await new Promise((resolve) => setTimeout(resolve, 100)); // 100ms 대기
    }
  }
}
async function getOption(page?: Page | Frame): Promise<ElementHandle[]> {
  const elements = await page?.$$("ul.content.scroll-y > div > li");
  if (elements) {
    const filteredElements: ElementHandle[] = await Promise.all(
      elements.filter(async (element) => {
        const className: string | undefined = await page?.evaluate(
          (el) => el.className,
          element
        );

        // 주어진 조건에 맞지 않는 클래스명을 가진 요소는 필터링합니다.
        return (
          className !== "month dimmed" &&
          className !== "day dimmed" &&
          className !== "day day-sat dimmed" &&
          className !== "day day-sun dimmed"
        );
      })
    );
    return filteredElements;
  }
  return [];
}
function isTimeInRange(time: string, range: string[]): boolean {
  console.log("time:::", time);
  const startTime = parseInt(range[0], 10);
  const endTime = parseInt(range[1], 10);
  const targetTime = parseInt(time, 10);
  console.log("startTime:::", startTime);
  console.log("endTime:::", endTime);
  console.log("targetTime:::", targetTime);
  console.log(targetTime >= startTime && targetTime <= endTime);

  return targetTime >= startTime && targetTime <= endTime;
}
