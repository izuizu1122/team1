$(document).ready(function() {
    // ページ読み込み時
    loadPageData();

    // イベントリスナー
    $('#ingredientForm').on('submit', saveIngredient);
    $('#cancelBtn').on('click', cancelEdit);
    $('#deleteItemBtn').on('click', deleteItem);

    // ページデータ読み込み
    function loadPageData() {
        // URLパラメータを取得（編集か新規作成か判定）
        const params = new URLSearchParams(window.location.search);
        const id = params.get('id');

        if (id) {
            // 編集モード
            $('#pageTitle').text('食材を編集');
            $('#deleteSection').show();
            
            // ダミーデータを表示（後で REST API に変更）
            loadIngredientData(id);
        } else {
            // 新規作成モード
            $('#pageTitle').text('食材を追加');
            $('#deleteSection').hide();
            
            // 購入日を今日に設定
            const today = new Date().toISOString().split('T')[0];
            $('#purchaseDate').val(today);
        }
    }

    // 食材データ読み込み
    function loadIngredientData(id) {
        // ダミーデータ（後で REST API に変更）
        const dummyData = {
            name: 'トマト',
            purchaseDate: '2026-04-10',
            expiryDate: '2026-04-25',
            quantity: 3,
            unit: '個',
            category: '野菜',
            memo: '冷蔵庫の野菜室に保管'
        };

        $('#ingredientName').val(dummyData.name);
        $('#purchaseDate').val(dummyData.purchaseDate);
        $('#expiryDate').val(dummyData.expiryDate);
        $('#quantity').val(dummyData.quantity);
        $('#unit').val(dummyData.unit);
        $('#category').val(dummyData.category);
        $('#memo').val(dummyData.memo);
    }

    // 食材保存
    function saveIngredient(e) {
        e.preventDefault();

        const ingredientName = $('#ingredientName').val();
        const purchaseDate = $('#purchaseDate').val();
        const expiryDate = $('#expiryDate').val();
        const quantity = $('#quantity').val();
        const unit = $('#unit').val();
        const category = $('#category').val();
        const memo = $('#memo').val();

        // バリデーション
        if (!ingredientName || !purchaseDate || !expiryDate) {
            alert('必須項目を入力してください');
            return;
        }

        // 賞味期限が購入日より後かチェック
        if (new Date(expiryDate) <= new Date(purchaseDate)) {
            alert('賞味期限は購入日より後に設定してください');
            return;
        }

        // 保存
        alert(ingredientName + ' を保存しました！');
        
        // 後で REST API に変更
        // $.ajax({
        //     url: 'http://localhost:5000/api/ingredients/save',
        //     method: 'POST',
        //     data: JSON.stringify({ ... }),
        //     ...
        // })

        // トップページに戻る
        window.location.href = 'index.html';
    }

    // キャンセル
    function cancelEdit() {
        if (confirm('編集をキャンセルしますか？')) {
            window.location.href = 'index.html';
        }
    }

    // 食材削除
    function deleteItem() {
        const ingredientName = $('#ingredientName').val();

        if (!confirm(ingredientName + ' を削除しますか？')) {
            return;
        }

        if (!confirm('本当に削除しますか？（再確認）')) {
            return;
        }

        alert(ingredientName + ' を削除しました');
        
        // 後で REST API に変更
        // $.ajax({
        //     url: 'http://localhost:5000/api/ingredients/delete/' + id,
        //     method: 'DELETE',
        //     ...
        // })

        window.location.href = 'index.html';
    }
});
