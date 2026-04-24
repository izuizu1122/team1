// トースト通知機能
function showToast(message, type = 'success', duration = 3000) {
    // コンテナがなければ作成
    if ($('.toast-container').length === 0) {
        $('body').append('<div class="toast-container"></div>');
    }

    // トースト要素を作成
    const $toast = $('<div>')
        .addClass('toast ' + type)
        .text(message);

    // コンテナに追加
    $('.toast-container').append($toast);

    // 指定時間後に削除
    setTimeout(function() {
        $toast.addClass('fadeOut');
        setTimeout(function() {
            $toast.remove();
        }, 300);
    }, duration);
}
