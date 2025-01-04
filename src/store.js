// 상태관리 파일
import { writable } from "svelte/store";

// 수정할 수 있는 값(초기값 : null)
export const user$ = writable(null);