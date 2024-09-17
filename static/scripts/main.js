import { app } from './init.js'
import { uid } from './auth.js'

import { getFirestore, doc, getDoc, setDoc, updateDoc, arrayUnion } from 'https://www.gstatic.com/firebasejs/10.13.1/firebase-firestore.js'
const db = getFirestore(app)

document.getElementById('send_button').addEventListener('click', async () => {
  const userref = doc(db, 'users', uid)
  const data = new Date()
  // ボタンを押したらその時刻が，db/users/UID/click に追加される
  const userdoc = await getDoc(userref)
  if (!userdoc.exists()) {
    // なければ作る
    await setDoc(userref, {click: [data]})
    console.log('new user', uid)
  } else {
    // あれば追加する
    await updateDoc(userref, {click: arrayUnion(data)})
    console.log('update user', uid)
  }
})