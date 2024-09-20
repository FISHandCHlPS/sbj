import { app } from './init.js'

import { getAuth, onAuthStateChanged, signInAnonymously } from 'https://www.gstatic.com/firebasejs/10.13.1/firebase-auth.js'

const auth = getAuth(app)

export let uid

onAuthStateChanged(auth, user => {
  if (user) {
    uid = user.uid
    console.log(uid)
  } else {
    signInAnonymously(auth)
  }
})