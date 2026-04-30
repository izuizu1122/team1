// ローディング画面機能
function showLoading(message = '処理中...') {
    // ローディングオーバーレイを作成
    const $overlay = $('<div>')
        .addClass('loading-overlay')
        .html('<div class="loading-content">' +
              '<div class="loading-spinner"></div>' +
              '<p>' + message + '</p>' +
              '</div>');
    
    $('body').append($overlay);
    
    return $overlay;
}

function hideLoading() {
    const $overlay = $('.loading-overlay');
    if ($overlay.length) {
        $overlay.addClass('hide');
        setTimeout(function() {
            $overlay.remove();
        }, 300);
    }
}

// ボタンのローディング状態
function setButtonLoading($btn, isLoading = true) {
    if (isLoading) {
        $btn.addClass('btn-loading').prop('disabled', true);
    } else {
        $btn.removeClass('btn-loading').prop('disabled', false);
    }
}
