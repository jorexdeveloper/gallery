/*
 * Wow
 */

// var $wow = new WOW().init();

/*
 * General
 */

var $container = $(".gallery-container").packery({
    itemSelector: ".gallery-item",
    columnWidth: ".gallery-item-sizer",
    gutter: ".gallery-gutter-sizer",
});

/*
 * Packery
 */

var $pckry = $container.data("packery");

$container
    .imagesLoaded()
    .progress(function (instance, image) {
        $container.packery("layout");
    })
    .always(function () {
        $container.packery("layout");
        // $pckry.find(".gallery-item").each(function (i, item) {
        //     var draggie = new Draggabilly(item);
        //     $pckry.packery("bindDraggabillyEvents", draggie);
        // });
        // console.log("Draggabilly events bound.");
    });

/*
 * Infinite Scroll
 */

var isLastPage = $container.data("last");
var currentPage = 0;

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
        append: ".gallery-item",
        outlayer: $pckry,
        prefill: true,
        // scrollThreshold: 100,
        // loadOnScroll: false,
        history: false,
        // historyTitle: false,
        status: ".page-load-status",
        button: ".view-more-button",
        checkLastPage: "#next-page-selector",
    });
}

initInfiniteScroll();
var $error = $(".infinite-scroll-error");

$container.on("request.infiniteScroll", function () {
    $error.addClass("visually-hidden");
});

$container.on("load.infiniteScroll", function (event, body, path, response) {
    currentPage += 1;
    isLastPage = $(body).find(".gallery-container").data("last");
    console.log(`Loaded page: ${path}, isLastPage=${isLastPage}`);
});

$container.on("error.infiniteScroll", function () {
    $error.removeClass("visually-hidden");
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
