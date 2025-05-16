// DOMの読み込みが完了したら実行
// 画像などの読み込みがある場合は'DomContentLoaded'の代わりに'load'を使う
window.addEventListener('DOMContentLoaded', () => {
    alert('DOMContentLoaded');
    // ボタン要素を取得
    const button = document.getElementById('testButton');
    
    // クリックイベントリスナーを追加
    button.addEventListener('click', handleClick);
});

// ボタンクリック時に実行される関数
function handleClick() {
    alert('ボタンがクリックされました！');
    //location.replace('/start');
}