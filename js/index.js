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
        window.location.href = 'edit.html';
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
        
        if (confirm(ingredientName + ' を削除しますか？')) {
            $(this).closest('.ingredient-card').fadeOut(300, function() {
                $(this).remove();
                showToast(ingredientName + ' を削除しました', 'success');
            });
        }
    });
});
