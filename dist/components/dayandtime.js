"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.selectDayTime = void 0;
const wait_1 = require("../utils/wait");
function selectDayTime(page, day, time) {
    return __awaiter(this, void 0, void 0, function* () {
        let movieReady = false;
        const frameElement = yield page.waitForSelector("iframe#ticket_iframe");
        const frame = yield (frameElement === null || frameElement === void 0 ? void 0 : frameElement.contentFrame());
        while (!movieReady) {
            const dayList = yield getOption(frame);
            const theDay = [];
            for (const yymmdd of dayList) {
                const dateAttribute = yield yymmdd.evaluate((el) => el.getAttribute("date"));
                console.log("DATE : " + dateAttribute);
                if (dateAttribute === null || dateAttribute === void 0 ? void 0 : dateAttribute.includes(day)) {
                    theDay.push(yymmdd);
                }
            }
            yield delayClick(theDay[0], "날짜");
            if (frame) {
                let list = yield frame.$$("div.theater > ul > li");
                while (list.length < 1) {
                    list = yield frame.$$("div.theater > ul > li");
                }
                for (const theTime of list) {
                    const playStartTime = yield theTime.evaluate((el) => el.getAttribute("play_start_tm"));
                    const countText = yield theTime.$eval("a > span.count", (element) => element.textContent || "");
                    if (playStartTime &&
                        isTimeInRange(playStartTime, [time[0], time[1]]) &&
                        countText !== "준비중") {
                        console.log("시작시간 찾음> >", playStartTime);
                        console.log(theTime);
                        movieReady = true;
                        yield (0, wait_1.waitThreeSeconds)();
                        yield delayClick(theTime, "시간");
                        break;
                    }
                }
            }
        }
        yield (0, wait_1.waitThreeSeconds)();
        const select = yield (frame === null || frame === void 0 ? void 0 : frame.$("a.btn-right.on"));
        console.log("SELECT:::", select);
        if (select) {
            console.log("SELECT:::", select);
            yield delayClick(select, "좌석선택");
        }
    });
}
exports.selectDayTime = selectDayTime;
function delayClick(element, comment) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log(`[${comment}]`);
        if (!element) {
            console.log("Element is null");
            return;
        }
        for (let i = 1; i <= 20; i++) {
            try {
                yield element.click();
                console.log(`${comment} 선택`);
                break; // 클릭에 성공하면 반복문을 종료합니다.
            }
            catch (error) {
                console.log(`${i}번째 ${comment} 선택 실패: `, error.message);
                // 실패한 경우에는 약간의 지연 후 다시 시도합니다.
                yield new Promise((resolve) => setTimeout(resolve, 100)); // 100ms 대기
            }
        }
    });
}
function getOption(page) {
    return __awaiter(this, void 0, void 0, function* () {
        const elements = yield (page === null || page === void 0 ? void 0 : page.$$("ul.content.scroll-y > div > li"));
        if (elements) {
            const filteredElements = yield Promise.all(elements.filter((element) => __awaiter(this, void 0, void 0, function* () {
                const className = yield (page === null || page === void 0 ? void 0 : page.evaluate((el) => el.className, element));
                // 주어진 조건에 맞지 않는 클래스명을 가진 요소는 필터링합니다.
                return (className !== "month dimmed" &&
                    className !== "day dimmed" &&
                    className !== "day day-sat dimmed" &&
                    className !== "day day-sun dimmed");
            })));
            return filteredElements;
        }
        return [];
    });
}
function isTimeInRange(time, range) {
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
