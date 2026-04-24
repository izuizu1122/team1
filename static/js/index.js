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

});