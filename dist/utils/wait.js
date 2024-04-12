"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.waitThreeSeconds = void 0;
function waitThreeSeconds() {
    return new Promise((resolve) => setTimeout(resolve, 3000));
}
exports.waitThreeSeconds = waitThreeSeconds;
