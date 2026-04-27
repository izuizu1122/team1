$(document).ready(function() {
    // ページ読み込み時
    loadPageData();

    // イベントリスナー
    // $('#ingredientForm').on('submit', saveIngredient);
    $('#cancelBtn').on('click', cancelEdit);
    $('#deleteItemBtn').on('click', deleteItem);
    
    // 写真関連のイベント
    $('#photo').on('change', previewPhoto);
    $('#removePhotoBtn').on('click', removePhoto);

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
            memo: '冷蔵庫の野菜室に保管',
            photoUrl: 'https://via.placeholder.com/300x250?text=トマト'
        };

        $('#ingredientName').val(dummyData.name);
        $('#purchaseDate').val(dummyData.purchaseDate);
        $('#expiryDate').val(dummyData.expiryDate);
        $('#quantity').val(dummyData.quantity);
        $('#unit').val(dummyData.unit);
        $('#category').val(dummyData.category);
        $('#memo').val(dummyData.memo);

        // ダミー写真を表示
        if (dummyData.photoUrl) {
            $('#previewImage').attr('src', dummyData.photoUrl);
            $('#photoPreview').show();
        }
    }

    // 写真プレビュー
    function previewPhoto(e) {
        const file = e.target.files[0];
        
        if (!file) {
            return;
        }

        // ファイルタイプチェック
        if (!file.type.startsWith('image/')) {
            showToast('画像ファイルのみアップロード可能です', 'error');
            $('#photo').val('');
            return;
        }

        // ファイルサイズチェック（5MB まで）
        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
            showToast('ファイルサイズは 5MB 以下にしてください', 'error');
            $('#photo').val('');
            return;
        }

        // プレビュー表示
        const reader = new FileReader();
        reader.onload = function(event) {
            $('#previewImage').attr('src', event.target.result);
            $('#photoPreview').show();
            showToast('写真をアップロードしました', 'success');
        };
        reader.readAsDataURL(file);
    }

    // 写真削除
    function removePhoto(e) {
        e.preventDefault();
        
        $('#photo').val('');
        $('#photoPreview').hide();
        $('#previewImage').attr('src', '');
        showToast('写真を削除しました', 'info');
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
        const photoFile = $('#photo')[0].files[0];

        // バリデーション
        if (!ingredientName || !purchaseDate || !expiryDate) {
            showToast('必須項目を入力してください', 'error');
            return;
        }

        // 賞味期限が購入日より後かチェック
        if (new Date(expiryDate) <= new Date(purchaseDate)) {
            showToast('賞味期限は購入日より後に設定してください', 'error');
            return;
        }

        // ローディング表示
        showLoading('保存中...');
        const $btn = $('.btn-save');
        const originalText = $btn.text();
        setButtonLoading($btn, true);

        // FormData を使って写真を含めて送信（後で REST API に変更）
        const formData = new FormData();
        formData.append('name', ingredientName);
        formData.append('purchaseDate', purchaseDate);
        formData.append('expiryDate', expiryDate);
        formData.append('quantity', quantity);
        formData.append('unit', unit);
        formData.append('category', category);
        formData.append('memo', memo);
        
        if (photoFile) {
            formData.append('photo', photoFile);
        }

        // 後で REST API に変更
        // $.ajax({
        //     url: 'http://localhost:5000/api/ingredients/save',
        //     method: 'POST',
        //     data: formData,
        //     processData: false,
        //     contentType: false,
        //     ...
        // })

        setTimeout(function() {
            hideLoading();
            setButtonLoading($btn, false);
            showToast(ingredientName + ' を保存しました', 'success');
            
            setTimeout(function() {
                window.location.href = '/';
            }, 1000);
        }, 1500);
    }

    // キャンセル
    function cancelEdit() {
        if (confirm('編集をキャンセルしますか？')) {
            showLoading('キャンセル中...');
            
            setTimeout(function() {
                hideLoading();
                showToast('キャンセルしました', 'info');
                
                setTimeout(function() {
                    window.location.href = '/';
                }, 500);
            }, 800);
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

        showLoading('削除中...');

        // 後で REST API に変更
        // $.ajax({
        //     url: 'http://localhost:5000/api/ingredients/delete/' + id,
        //     method: 'DELETE',
        //     ...
        // })

        setTimeout(function() {
            hideLoading();
            showToast(ingredientName + ' を削除しました', 'success');
            
            setTimeout(function() {
                window.location.href = '/';
            }, 1000);
        }, 1500);
    }
});
