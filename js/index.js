$(document).ready(function() {
    // 検索機能
    $('#searchInput').on('keyup', function() {
        const searchTerm = $(this).val().toLowerCase();
        
        $('.ingredient-card').each(function() {
            const ingredientName = $(this).find('h3').text().toLowerCase();
            
            if (ingredientName.includes(searchTerm)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // 新規追加ボタン
    $('#addBtn').on('click', function() {
        showLoading('食材追加ページへ移動中...');
        setTimeout(function() {
            hideLoading();
            window.location.href = 'edit.html';
        }, 800);
    });

    // 編集ボタン
    $('.btn-edit').on('click', function() {
        const ingredientName = $(this).closest('.ingredient-card').find('h3').text();
        showToast(ingredientName + ' を編集します', 'info');
        // 後で: window.location.href = 'edit.html?id=xxx';
    });

    // 削除ボタン
    $('.btn-delete').on('click', function() {
        const ingredientName = $(this).closest('.ingredient-card').find('h3').text();
        const $card = $(this).closest('.ingredient-card');
        
        if (confirm(ingredientName + ' を削除しますか？')) {
            showLoading('削除中...');
            
            setTimeout(function() {
                $card.fadeOut(300, function() {
                    $(this).remove();
                    hideLoading();
                    showToast(ingredientName + ' を削除しました', 'success');
                });
            }, 500);
        }
    });
});
