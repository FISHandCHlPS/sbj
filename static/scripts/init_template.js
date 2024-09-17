import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.1/firebase-app.js"

// 自分の設定に書き換えて init.js とする
export const app = initializeApp({
  apiKey: "APIKEY",
  authDomain: "PROJECTID.firebaseapp.com",
  projectId: "PROJECTID",
  storageBucket: "PROJECTID.appspot.com",
  messagingSenderId: "MESSAGINGSENDERID",
  appId: "APPID",
  measurementId: "MEASUREMENTID",
})