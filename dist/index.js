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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const login_1 = __importDefault(require("./components/login"));
const findMovie_1 = require("./components/findMovie");
const init_1 = require("./components/init");
const dayandtime_1 = require("./components/dayandtime");
const MOVIENAME = "듄-파트2";
// 메인 로직
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        const { browser, page } = yield (0, init_1.startBrowser)();
        yield (0, login_1.default)(page);
        yield (0, findMovie_1.findMovie)(page, MOVIENAME);
        yield (0, dayandtime_1.selectDayTime)(page, "20240330", ["2100", "2500"]);
        // 필요한 작업을 마친 후 브라우저 종료
        yield browser.close();
    });
}
main().catch(console.error);
