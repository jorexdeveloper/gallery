/*
 * Wow
 */

// var $wow = new WOW().init();

/*
 * Packery
 */

var $container = $(".gallery-container").packery({
    itemSelector: ".gallery-item",
    columnWidth: ".gallery-item-sizer",
    gutter: ".gallery-gutter-sizer",
});
var $pckry = $container.data("packery");

/*
 * Images Loaded
 */

$container
    .imagesLoaded()
    .progress(function () {
        $container.packery("layout");
    })
    .always(function () {
        $container.packery("layout");
        // $container.find(".gallery-item").each(function (i, item) {
        //     var draggie = new Draggabilly(item);
        //     $container.packery("bindDraggabillyEvents", draggie);
        // });
    });

/*
 * Infinite Scroll
 */

var currentPage = 0;
var isLastPage = $container.data("last");

function initInfiniteScroll() {
    $container.infiniteScroll({
        path: function () {
            if (!isLastPage) {
                var url = $container.data("url");
                var path = $container.data("path");
                var pageNumber = currentPage + 1;

                return `${url}?path=${path}&page=${pageNumber}`;
            }
        },
        prefill: true,
        append: ".gallery-item",
        // scrollThreshold: 100,
        // loadOnScroll: false,
        // historyTitle: false,
        status: ".page-load-status",
        button: ".view-more-button",
        checkLastPage: "#next-page-selector",
        outlayer: $pckry,
        history: false,
    });
}

initInfiniteScroll();

var $scrollError = $(".infinite-scroll-error");

$container.on("request.infiniteScroll", function () {
    $scrollError.addClass("visually-hidden");
});

$container.on("load.infiniteScroll", function (event, body) {
    currentPage += 1;
    isLastPage = $(body).find(".gallery-container").data("last");
});

$container.on("error.infiniteScroll", function () {
    $scrollError.removeClass("visually-hidden");
});

$("#retry-button").on("click", function () {
    $container.infiniteScroll("destroy");
    initInfiniteScroll();
    $container.infiniteScroll("loadNextPage");
});

/*
 * Fancybox
 */

Fancybox.bind("[data-fancybox]", {
    closeExisting: true,
    idle: 3000,
    // TODO: Responsive thumbnails

    mainStyle: {
        "--f-toolbar-padding": "8px",
        "--f-toolbar-gap": "8px",
        "--f-button-border-radius": "50%",
        "--f-thumb-width": "82px",
        "--f-thumb-height": "82px",
        "--f-thumb-opacity": "0.5",
        "--f-thumb-hover-opacity": "1",
        "--f-thumb-selected-opacity": "1",
    },

    Carousel: {
        Toolbar: {
            display: {
                left: ["counter"],
                middle: [],
                right: [
                    "autoplay",
                    "fullscreen",
                    "thumbs",
                    "download",
                    "close",
                ],
            },
        },

        Zoomable: {
            Panzoom: {
                clickAction: "false",
                dblClickAction: "iterateZoom",
                maxScale: 1,
            },
        },
    },
});
