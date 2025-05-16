'use strict'

firebase.initializeApp({
    apiKey:  "AIzaSyAGHsi_Nk_OcR8Hcqr16FZTALqJWszRM0w",
    authDomain: "alien-legacy-366606.firebaseapp.com",
    databaseURL: "https://alien-legacy-366606.firebaseio.com",
    projectId: "alien-legacy-366606",
    storageBucket: "alien-legacy-366606.appspot.com",
    messagingSenderId: "39218554993",
    appId: "1:39218554993:web:dd7c1ee84bd4f1330bd3d0",
    measurementId: "G-D6Q91XW5RR",
})

const num_iteration = 100;

window.onload = () => {

    const cardId = ["playerCard1Front","playerCard1Back",
                    "playerCard2Front","playerCard2Back",
                    "houseCard1Front","houseCard1Back",
                    "houseCard2Front","houseCard2Back"];
    const intervenue_type = 1 + Math.floor(Math.random() * 2);
    //console.log("intervenue_type", ["non", "active", "passive"][intervenue_type])

    var TOKEN;
    var sessionId = 0;
    var point = 1000;
    var action = -1;
    var Cards = [1,1,2,2]
    var exp_type = null
    var result = {
        dummy: 'yyy',
    }

    document.getElementById("disp2").style.display='none'
    document.getElementById("disp3").style.display='none'
    document.getElementById("disp4").style.display='none'
    document.getElementById("disp5").style.display='none'
    document.getElementById("stop").style.display='none'
    document.getElementById("resultWord_red").style.display = 'none'
    document.getElementById("resultWord_blue").style.display = 'none'

    // 通信用APIを定義
    // POST[data] -> 成功時にsuccess( res.json() )
    function call_api(name, data, success, fail) {
        data['token'] = TOKEN
        //console.log("api start", name, data)
        return fetch('/api/' + name, {
            method: 'POST',
            body: JSON.stringify(data),
        }).then((res) => {
            if (res.ok) {
                return res.json()
            }
            throw 'not ok'
        }).then((data) => {
            //console.log("api end", name, data)
            success(data)
        }).catch((err) => {
            //console.log(err)
            fail()
        })
    }
    
    function deal_cards(){
        var arr = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9];
        var a = arr.length;
        
        while (a){
            var j = Math.floor(Math.random() * a);
            var t = arr[--a];
            arr[a] = arr[j];
            arr[j] = t;
        }
        return arr.slice(0,2);
    }

    function deal_cards_both() {
        var [a,b] = deal_cards();
        var [c,d] = deal_cards();
        Cards[0] = a;
        Cards[1] = b;
        Cards[2] = c;
        Cards[3] = d;
        //console.log("Deal:", Cards.slice(0,3))
    }
    
    function get_point(act){
        var [c,d,a,b] = Cards
        if (act==1){
            if (a+b<c+d){
                return 100
            } else if (a+b==c+d){
                return -30
            }else{
                return -70
            }
        } else{
            return -30
        }
    }
    function get_result(act){
        var [c,d,a,b] = Cards
        if (act==1){
            if (a+b<c+d){
                document.getElementById("resultWord").style.display = 'none'
                document.getElementById("resultWord_red").style.display = 'block'
            } else if (a+b==c+d){
                document.getElementById("resultWord").innerText = "引き分け"
            }else{
                document.getElementById("resultWord").style.display = 'none'
                document.getElementById("resultWord_blue").style.display = 'block'
            }
        } else{
            document.getElementById("resultWord").innerText = "降り"
        }
    }

    let start_button = document.getElementById('start')
    let next_button = document.getElementById('next')
    let finish_button = document.getElementById('finish')
    let stop_button = document.getElementById('stop')
    var bet_button_normal = document.getElementById('betNormal')
    var fold_button_normal = document.getElementById('foldNormal')
    var bet_button_rec = document.getElementById('betRec')
    var fold_button_rec = document.getElementById('foldRec')

    function success_login() {
        //console.log('login')
        start_button.disabled = false
    }

    function fail_login() {
        //console.log('error_login')
    }

    function before_start() {
        //console.log('before_start')
        start_button.disabled = true
    }

    function success_start(data) {
        exp_type = data['exp_type']
        //console.log('after_start')
        finish_button.disabled = false
    }

    function fail_start() {
        firebase.auth().signOut();
        //console.log('error_start')
    }
    
    function success_session() {
        //console.log('sucess session');
    }

    function fail_session() {
        //console.log('fail session')
        firebase.auth().signOut();
    }

    function success_intervenue(data) {
        if (data==null || intervenue_type==0){
            bet_button_normal.style.display = 'block'
            fold_button_normal.style.display = 'block'
            bet_button_rec.style.display = 'none'
            fold_button_rec.style.display = 'none'
            bet_button_normal.disabled = false;
	        fold_button_normal.disabled = false;
        }else if (data["intervenue"]==1){
            bet_button_normal.style.display = 'none'
            fold_button_normal.style.display = 'block'
            bet_button_rec.style.display = 'block'
            fold_button_rec.style.display = 'none'
            bet_button_rec.disabled = false;
	        fold_button_normal.disabled = false;
        }else if (data["intervenue"]==0){
            bet_button_normal.style.display = 'block'
            fold_button_normal.style.display = 'none'
            bet_button_rec.style.display = 'none'
            fold_button_rec.style.display = 'block'
            bet_button_normal.disabled = false;
	        fold_button_rec.disabled = false;
        }else{
            bet_button_normal.style.display = 'block'
            fold_button_normal.style.display = 'block'
            bet_button_rec.style.display = 'none'
            fold_button_rec.style.display = 'none'
            bet_button_normal.disabled = false;
	        fold_button_normal.disabled = false;
        }
        //console.log('sucess intervenue');
    }

    function fail_intervenue() {
        //console.log('fail intervenue')
        firebase.auth().signOut();
    }

    function before_finish() {
        //console.log('before_finish')
        finish_button.disabled = true
    }

    function success_finish(data) {
    	document.getElementById('finalScore').innerText = String(point);
        document.getElementById("YourId").innerText = data['uid']
        //console.log('after_finish')
    }

    function fail_finish() {
        //console.log('error_finish')
        firebase.auth().signOut();
    }
    
    function main_session(action) {
        bet_button_normal.disabled = true;
        fold_button_normal.disabled = true;
        bet_button_rec.disabled = true;
        fold_button_rec.disabled = true;
        
        point += get_point(action);
        sessionId += 1;
        
        //console.log("Check:", Cards, "action", action);
        call_api(
            "session",
            {
                "token":TOKEN,
                "session_id":sessionId,
                "intervenue_type": intervenue_type,
                "playerCard1":Cards[0],
                "playerCard2":Cards[1],
                "houseCard1":Cards[2],
                "houseCard2":Cards[3],
                "dif":Cards[0] + Cards[1] - Cards[2],
                "action":action,
                "point":point,
            },
            success_session, fail_session,
        ).then(()=>{
            document.getElementById(cardId[7]).style.display='none';
            document.getElementById(cardId[6]).style.display='block';
            document.getElementById(cardId[6]).innerText = String(Cards[3]);
            document.getElementById('numPoint').innerText = String(point);
            success_session();
            document.getElementById('numPoint').innerText = String(point-get_point(action))+"→"+String(point);
            get_result(action);
            
            setTimeout(function(){
                for (let i=0;i<8;i++){
                    if (i%2==0){
                        document.getElementById(cardId[i]).style.display='none';
                    }else{
                        document.getElementById(cardId[i]).style.display='block';
                    }
                }
                document.getElementById("resultWord_red").style.display = 'none'
                document.getElementById("resultWord_blue").style.display = 'none'
                document.getElementById("resultWord").style.display = 'block'

                document.getElementById('resultWord').innerText = 'シャッフル中...';
                setTimeout(function(){
	                if (sessionId+1 > num_iteration){
	                    document.getElementById("disp3").style.display='none'
	                    document.getElementById("stop").style.display='none'
	                    document.getElementById("disp4").style.display='block'
	                }else{
                        deal_cards_both()
				        for (let i=0; i<6; i++){
			                if (i%2==0){
			                    document.getElementById(cardId[i]).style.display = 'block'
			            	    document.getElementById(cardId[i]).innerText = String(Cards[Math.floor(i/2)]);
			            	}else{
			            	    document.getElementById(cardId[i]).style.display = 'none'
			            	}
			            }
		                document.getElementById('numPoint').innerText = String(point);
		                document.getElementById('resultWord').innerText = '勝負する？/勝負から降りる？';
		                document.getElementById('num_iter').innerText = String(sessionId+1)+"/"+String(num_iteration);
		                
		                call_api(
                            "intervenue",
                            {
                                "token":TOKEN,
                                "session_id": sessionId+1,
                                "playerCard1":Cards[0],
                                "playerCard2":Cards[1],
                                "houseCard1":Cards[2],
                                "houseCard2":Cards[3],
                                "action":action,
                                "dif":Cards[0] + Cards[1] - Cards[2],
                                "intervenue_type":intervenue_type,
                            },
                            success_intervenue, fail_intervenue,
                        );
	                }
                },1500);
            },2500);
        }).catch(()=>{
            //console.log("api error..?")
        })
    }

    start_button.addEventListener('click', () => {
        before_start()
        call_api('start', {token: TOKEN}, success_start, fail_start)
        document.getElementById("disp1").style.display='none'
        document.getElementById("disp2").style.display='block'
        document.getElementById("stop").style.display='block'
    }, false)
    
    
    next_button.addEventListener('click',() => {
        document.getElementById("disp2").style.display='none';
        document.getElementById("disp3").style.display='block';
        bet_button_normal.style.display = 'block'
        fold_button_normal.style.display = 'block'
        bet_button_rec.style.display = 'none'
        fold_button_rec.style.display = 'none'
        
        for (let i=0;i<8;i++){
            if (i%2==0){
                document.getElementById(cardId[i]).style.display='none';
            }else{
                document.getElementById(cardId[i]).style.display='block';
            }
        }

        deal_cards_both()
        
        call_api(
            "intervenue",
            {
                "token": TOKEN,
                "session_id": sessionId+1,
                "intervenue_type":intervenue_type,
                "playerCard1": Cards[0],
                "playerCard2": Cards[1],
                "houseCard1": Cards[2],
                "houseCard2": Cards[3],
                "dif": Cards[0] + Cards[1] - Cards[2],
            },
            success_intervenue, fail_intervenue,
        ).then(() => {
            setTimeout(() => {
                for (let i=0; i<6; i++){
                    if (i%2==0){
                        document.getElementById(cardId[i]).style.display = 'block'
                        document.getElementById(cardId[i]).innerText = String(Cards[Math.floor(i/2)]);
                    }else{
                        document.getElementById(cardId[i]).style.display = 'none'
                    }
                }
                document.getElementById('numPoint').innerText = String(point);
                document.getElementById('num_iter').innerText = "1/"+String(num_iteration);
                document.getElementById('resultWord').innerText = '勝負する？/勝負から降りる？';
                var action = -1;
                bet_button_normal.disabled = false;
                fold_button_normal.disabled = false;

                call_api(
                    "session",
                    {
                        "token": TOKEN,
                        "session_id": sessionId,
                        "intervenue_type": intervenue_type,
                        "playerCard1": 0,
                        "playerCard2": 0,
                        "houseCard1": 0,
                        "houseCard2": 0,
                        "dif": -100,
                        "action": -1,
                        "point": 1000,
                    },
                    success_session, fail_session
                )
            }, 1000)
        })
    }, false)
    
    stop_button.addEventListener('click', () => {
        document.getElementById("disp2").style.display='none'
        document.getElementById("disp3").style.display='none'
        document.getElementById("disp5").style.display='block'
        document.getElementById("stop").style.display='none'
        var data = {
            token: TOKEN,
            exp_type: exp_type,
            result: point,
        }
        before_finish()
        call_api('finish', data, success_finish, fail_finish)
        firebase.auth().signOut();
    }, false)

    bet_button_normal.onclick = function(){
        action = 1;
        main_session(action);
    }
    
    fold_button_normal.onclick = function(){
        action = 0;
        main_session(action)
    }
    
    bet_button_rec.onclick = function(){
        action = 1;
        main_session(action);
    }
    
    fold_button_rec.onclick = function(){
        action = 0;
        main_session(action)
    }

    finish_button.addEventListener('click', () => {
        before_finish()
        call_api(
            'finish',
            {
                token: TOKEN,
                exp_type: exp_type,
                result: point,
            },
            success_finish, fail_finish,
        )
        firebase.auth().signOut();
    }, false)

    firebase.auth().onAuthStateChanged(user => {
        if (user) {
            user.getIdToken().then(function(token){
                TOKEN = token
            });
            //console.log(user.uid)
            success_login()
        }
    })

    firebase.auth().signOut().then(() => {
        firebase.auth().signInAnonymously().catch(fail_login)
    })
}
