var movieRecommender = {
    init:function(){
        this.event();
    },
    event:function(){
        $('#recommendBtn').click(function(){
            movieRecommender.fnRecommend();
        })
        $('#movieTitle').on('keyup', function() {
            const query = $(this).val().trim();
            if (query.length > 0) {
                movieRecommender.fnMovieTitle(query);
            } else {
                return;
            }
        });
        $(document).on('click', '.autocomplete-item', function() {
            const selectedTitle = $(this).text();
            $('#movieTitle').val(selectedTitle);         // input에 반영
            $('.autocomplete-list').hide();               // 목록 숨기기
        });
    },
    fnRecommend:function(){
        const movieTitle = $('#movieTitle').val();
        $.ajax({
            url : "/movieRecommend",
            type : "POST",
            cache : false,
            dataType : "json",
            data : JSON.stringify({'movieTitle':movieTitle}),
            contentType : "application/json",
            beforeSend : function(){},
            success : function(result){
                movieRecommender.fnDrawResult(result);
            },
            error : function(request, status){
                alert("오류가 발생하였습니다. ["+request.status +"]");
                console.log(">>>>>>>> setRecommend error dtata : "+status);
            },
            complete: function(){

            }
        })
    },
    fnDrawResult : function(result){
        if(result.result==''){
            alert('영화 제목을 정확히 입력해주세요.')
            return;
        }
        $('#result-container').empty(); // 이전 결과 지움
        
        result.result.forEach(movie => {
            var avg = movie['Average Rating'];
            var full = Math.floor(avg);
            var half = avg - full >= 0.5 ? 1 : 0;
            var empty = 5 - full - half;

            var stars = '★'.repeat(full) + (half ? '⯨ ' : '') + '☆'.repeat(empty);
            
            const genres = movie.Genres.split('|');
            const badges = genres.map(g => `<span class="genre-badge">${g}</span>`).join('');
            const hashtags = (movie.Tag || []).map(tag => `<span class="hashtag-badge">#${tag}</span>`).join('');

            $('#result-container').append(`
                <div class="movie-card">
                    <div class="title">${movie.Title}<span class="year">(${movie.Year})</span></div>
                    <div class="genres">${badges}</div>
                    <div class="rating"> ${stars}<span class="rating-number">(${ movie['Rating Count'] })</span> </div>
                    <div class="info">
                        <span><strong>Rank:</strong> ${ movie.Rank }</span><br>
                        <span><strong>Similarity:</strong> ${ movie.Similarity }</span>
                    </div>
                    <div class="hashtags">${hashtags}</div> 
                </div>
            `);
        })
    },
    fnMovieTitle : function(query){
        $.ajax({
            url : "/movieTitle",
            type : "POST",
            cache : false,
            dataType : "json",
            data : JSON.stringify({'query':query}),
            contentType : "application/json",
            beforeSend : function(){},
            success : function(result){
                movieRecommender.fnDrawAutoTitle(result);
            },
            error : function(request, status){
                alert("오류가 발생하였습니다. ["+request.status +"]");
                console.log(">>>>>>>> setRecommend error dtata : "+status);
            },
            complete: function(){

            }
        })
    },
    fnDrawAutoTitle : function(result){
        $('#autocompleteTitle').empty();
        result.forEach(title => {
            $('#autocompleteTitle').append(`
                <li class="autocomplete-item">${title}</li>
            `);
        })
        $('#autocompleteTitle').show();      
    }
}