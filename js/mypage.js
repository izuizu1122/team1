$(document).ready(function() {
    // ページ読み込み時にデータを表示
    loadUserProfile();

    // イベントリスナー
    $('#saveSetting').on('click', saveSetting);
    $('#changePasswordBtn').on('click', changePassword);
    $('#deleteAccountBtn').on('click', deleteAccount);

    // ユーザープロフィール読み込み
    function loadUserProfile() {
        // ダミーデータ（後で REST API に変更）
        $('#userName').text('田中太郎');
        $('#userEmail').text('tanaka@example.com');
        $('#totalIngredients').text('6');
        $('#warningIngredients').text('2');
        $('#expiredIngredients').text('0');
    }

    // 設定保存
    function saveSetting() {
        const notificationDays = $('#notificationDays').val();
        const theme = $('#theme').val();

        showToast('設定を保存しました', 'success');
        
        // 後で REST API に変更
        // $.ajax({ ... })
    }

    // パスワード変更
    function changePassword() {
        const newPassword = prompt('新しいパスワードを入力してください:');
        
        if (!newPassword) {
            return;
        }

        if (newPassword.length < 6) {
            showToast('パスワードは6文字以上にしてください', 'error');
            return;
        }

        showToast('パスワードを変更しました', 'success');
        
        // 後で REST API に変更
        // $.ajax({ ... })
    }

    // アカウント削除
    function deleteAccount() {
        const confirmed = confirm('本当にアカウントを削除しますか？\nこの操作は取り消せません。');
        
        if (!confirmed) {
            return;
        }

        const doubleConfirmed = confirm('本当に削除しますか？（再確認）');
        
        if (doubleConfirmed) {
            showToast('アカウントを削除しました', 'success');
            // 後で REST API に変更
            // window.location.href = 'login.html';
        }
    }
});
