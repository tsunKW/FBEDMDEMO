/*
 * 精簡版 navlight 
 * 只保留：1. 選單吸頂功能 (topSuction)  2. 錨點滑動與高亮連動 (navLight)
 */

// 1. 導覽/選單--置頂組件 (保留原版吸頂邏輯)
$.fn.topSuction = function(option) {
    option = option || {};
    var fixCls = option.fixCls || 'cate-fixed'; 
    var $self = this;
    var $win  = $(window);
    if (!$self.length) return;

    var offset = $self.offset();
    var fTop   = offset.top;

    function fix(){
        var dTop = $(document).scrollTop();
        if ( fTop < dTop ) {
            $self.addClass(fixCls);
        } else {
            $self.removeClass(fixCls);
        };
    }
    fix();
    $win.scroll(function() { fix(); });
    $win.resize(function() { 
        fTop = $self.offset().top; 
        fix(); 
    });
};

// 節流與防抖 (效能優化)
$.debounce = function(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};
$.throttle = function(func, wait) {
    var context, args, timeout, throttling, more, result;
    var whenDone = $.debounce(function() { more = throttling = false; }, wait);
    return function() {
        context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (more) func.apply(context, args);
            whenDone();
        };
        if (!timeout) timeout = setTimeout(later, wait);
        if (throttling) { more = true; } else { result = func.apply(context, args); };
        whenDone();
        throttling = true;
        return result;
    };
};

// 2. 導覽/選單--高亮與點擊滑動組件
$.fn.navLight = function(option) {
    option = option || {};
    var navarea = option.navarea || '.NavArea';      // 選單外層
    var nav = option.nav || '.nav-btn';              // 你的 a 標籤
    var content = option.content || '.js-content';   // 對應的內容區塊
    var lightCls = option.lightCls || 'cate-hover';  // 高亮時的 Class
    var top_i = option.top_i || 0;                   // 點擊後距離頂部的偏移量(避開吸頂選單)
    var top_timing = option.top_timing || 500;       // 滑動速度

    var $self = $(this);
    var $navarea = $self.find(navarea);
    var $nav = $navarea.find(nav);
    var $content = $self.find(content);
    var $win = $(window);
    var $doc = $(document);

    // 取得所有區塊的高度位置
    var contentPosi = {};
    function contentPosiFu(){ 
        contentPosi = $content.map(function(idx, elem) {
            var $cont = $(elem);
            var top = $cont.offset().top;
            return {
                top: top - top_i - 50, // 容錯範圍
                bottom: top + $cont.outerHeight()
            };
        }); 
    }

    // 捲動時判斷高亮
    var handler = $.throttle(function(e) {
        var dTop = $doc.scrollTop();
        contentPosiFu();
        
        contentPosi.each(function(idx, posi) {
            if ( posi.top < dTop && posi.bottom > dTop ) {
                $nav.removeClass(lightCls);
                $nav.eq(idx).addClass(lightCls);
            }
        });

        // 頁面到底時，強制高亮最後一個
        if( dTop + window.innerHeight >= $doc.height() - 10 ){
            $nav.removeClass(lightCls);
            $nav.eq(contentPosi.length-1).addClass(lightCls);
        }
    }, 100);

    // 點擊選單滑動
    $navarea.delegate(nav, 'click', function(e) {
        e.preventDefault();
        contentPosiFu(); 
        var idx = $nav.index(this); // 抓取點擊的是第幾個 a
        var $cont = $content.eq(idx); // 對應第幾個區塊
        
        if($cont.length > 0) {
            var targetTop = $cont.offset().top;
            $('html,body').stop().animate({ scrollTop: targetTop - top_i }, top_timing);
        }
    });

    $win.scroll(handler);
};