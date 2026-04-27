$(document).ready(function() {
    // 簡易的な漢字→ひらがな変換（よくある食材用）
    const kanji2Hiragana = {
        'トマト': 'とまと',
        '玉ねぎ': 'たまねぎ',
        '塩': 'しお',
        'キャベツ': 'きゃべつ',
        'ニンジン': 'にんじん',
        '牛乳': 'ぎゅうにゅう'
    };

    // 検索機能（ひらがな対応）
    $('#searchInput').on('keyup', function() {
        const searchTerm = $(this).val().toLowerCase();
        
        $('.ingredient-card').each(function() {
            const ingredientName = $(this).find('h3').text();
            const ingredientNameLower = ingredientName.toLowerCase();
            
            // ひらがな変換
            let ingredientHiragana = kanji2Hiragana[ingredientName] || ingredientNameLower;
            
            // 検索
            if (ingredientNameLower.includes(searchTerm) || 
                ingredientHiragana.includes(searchTerm)) {
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
            window.location.href = 'http://localhost:5000/add';
        }, 800);
    });

    // 編集ボタン
    $('.btn-edit').on('click', function() {
        const ingredientName = $(this).closest('.ingredient-card').find('h3').text();
        showToast(ingredientName + ' を編集します', 'info');
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
