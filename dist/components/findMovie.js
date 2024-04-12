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
exports.findMovie = void 0;
const wait_1 = require("../utils/wait");
function findMovie(page, name) {
    return __awaiter(this, void 0, void 0, function* () {
        yield page.goto("http://www.cgv.co.kr/ticket/");
        // iframe으로 전환
        const frameElement = yield page.waitForSelector("iframe#ticket_iframe");
        const frame = yield (frameElement === null || frameElement === void 0 ? void 0 : frameElement.contentFrame());
        let passValue = false;
        // 영화 목록 로딩 대기
        const movieListSelector = "div.movie-list.nano.has-scrollbar.has-scrollbar-y > ul > li";
        yield (frame === null || frame === void 0 ? void 0 : frame.waitForSelector(movieListSelector, { visible: true }));
        const movieList = yield (frame === null || frame === void 0 ? void 0 : frame.$$(movieListSelector));
        if (movieList) {
            for (const movie of movieList) {
                const movieText = yield (yield movie.getProperty("textContent")).jsonValue();
                if ((movieText === null || movieText === void 0 ? void 0 : movieText.includes(name)) && !movieText.includes("[")) {
                    yield movie.evaluate((movieElement) => {
                        var _a;
                        (_a = movieElement.querySelector("a")) === null || _a === void 0 ? void 0 : _a.click();
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
            yield (frame === null || frame === void 0 ? void 0 : frame.waitForSelector("div.checkedBD", {
                timeout: 5000,
                visible: true,
            }));
            const imaxButton = yield (frame === null || frame === void 0 ? void 0 : frame.$('li#sbmt_imax > a[data-type="IMAX"]'));
            yield (0, wait_1.waitThreeSeconds)();
            yield (imaxButton === null || imaxButton === void 0 ? void 0 : imaxButton.click());
            yield (0, wait_1.waitThreeSeconds)();
            passValue = true;
        }
        catch (error) {
            console.log("IMAX 옵션이 없습니다.");
            passValue = false;
        }
        if (!passValue) {
            return false;
        }
        // 극장 선택
        try {
            const theaterSelector = 'li[theater_cd="0013"]';
            yield (frame === null || frame === void 0 ? void 0 : frame.waitForSelector(theaterSelector, { timeout: 5000 }));
            yield (frame === null || frame === void 0 ? void 0 : frame.click(theaterSelector));
            yield (0, wait_1.waitThreeSeconds)();
            yield page.screenshot({ path: "2222.png" });
            passValue = true;
        }
        catch (error) {
            console.log("극장을 선택할 수 없습니다.");
            passValue = false;
        }
        return passValue;
    });
}
exports.findMovie = findMovie;
