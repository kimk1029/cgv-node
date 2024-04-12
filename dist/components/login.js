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
const ID = "kimk1029";
const PASSWORD = "aormsja!4";
function login(page) {
    return __awaiter(this, void 0, void 0, function* () {
        const loginUrl = "https://www.cgv.co.kr/user/login/";
        yield page.goto(loginUrl, { waitUntil: "networkidle2" });
        // 로그인 과정
        yield page.type("#txtUserId", ID);
        yield page.type("#txtPassword", PASSWORD);
        const navigationPromise = page.waitForNavigation();
        yield Promise.all([
            page.click("#submit"), // 로그인 버튼 클릭
            navigationPromise, // 다음 페이지로의 이동이 완료될 때까지 기다림
        ]);
        yield page.screenshot({ path: "example1.png" });
        // 추가적인 대기 조건이 필요하다면 여기에 구현
    });
}
exports.default = login;
