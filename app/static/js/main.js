/*
 * Wow
 */

// var $wow = new WOW().init();

/*
 * Packery
 */

var gallery = $(".gallery-container").packery({
    itemSelector: ".gallery-item",
    columnWidth: ".gallery-item-sizer",
    gutter: ".gallery-gutter-sizer",
});

var packery = gallery.data("packery");

/*
 * Infinite Scroll
 */

var infiniteScroll;
var currentPage = 0;
var isLastPage = gallery.data("last");
var isLoading = false;
var dirRecurse = false;

function initInfiniteScroll() {
    infiniteScroll = gallery
        .infiniteScroll({
            path: function () {
                if (!isLastPage) {
                    var url = gallery.data("url");
                    var path = gallery.data("path");
                    var pageNumber = currentPage + 1;

                    if (dirRecurse)
                        return `${url}?path=${path}&page=${pageNumber}&recurse=${dirRecurse}`;
                    else return `${url}?path=${path}&page=${pageNumber}`;
                }
            },
            prefill: true,
            append: ".gallery-item",
            status: ".page-load-status",
            checkLastPage: "#next-page-selector",
            outlayer: packery,
            history: false,
        })
        .data("infiniteScroll");
}

initInfiniteScroll();

gallery.on("request.infiniteScroll", function () {
    isLoading = true;
    $(".infinite-scroll-error").addClass("d-none");
});

gallery.on("load.infiniteScroll", function (event, body) {
    currentPage += 1;
    isLoading = false;
    isLastPage = $(body).find(".gallery-container").data("last");
});

gallery.on("error.infiniteScroll", function () {
    isLoading = false;
    $(".infinite-scroll-error").removeClass("d-none");
});

$("#retry-button").on("click", function () {
    gallery.infiniteScroll("destroy");
    initInfiniteScroll();
    gallery.infiniteScroll("loadNextPage");
});

/*
 * Fancybox
 */

var colorWorker = new Worker("/static/js/color-worker.js");
var useImageBg = false;

Fancybox.bind("[data-fancybox]", {
    idle: 3000,
    closeExisting: true,
    theme: "dark",
    Hash: false,

    Carousel: {
        Thumbs: false,
        transition: "tween",
        // vertical: true,
        // dragFree: true,
        // fill: true,

        Toolbar: {
            display: {
                left: ["autoplay"],
                middle: [],
                right: ["fullscreen", "download", "close"],
            },
        },

        // Arrows: false,

        Zoomable: {
            Panzoom: {
                clickAction: "false",
                dblClickAction: "iterateZoom",
                protected: true,
                maxScale: 1,
            },
        },

        breakpoints: {
            "(min-width: 768px)": {
                vertical: false,

                Toolbar: {
                    display: {
                        left: ["autoplay"],
                        middle: [],
                        right: ["fullscreen", "thumbs", "download", "close"],
                    },
                },

                Thumbs: {
                    showOnStart: false,
                },
            },

            "(min-width: 1024px)": {
                vertical: false,

                Toolbar: {
                    display: {
                        left: ["autoplay"],
                        middle: [
                            "zoomIn",
                            "zoomOut",
                            "toggle1to1",
                            "rotateCCW",
                            "rotateCW",
                            "flipX",
                            "flipY",
                        ],
                        right: ["fullscreen", "thumbs", "download", "close"],
                    },
                },

                Thumbs: {
                    showOnStart: true,
                },

                Zoomable: {
                    Panzoom: {
                        clickAction: "iterateZoom",
                        dblClickAction: "false",
                        protected: true,
                        maxScale: 1,
                    },
                },
            },
        },

        on: {
            render: () => {
                if (useImageBg) {
                    var img = Fancybox.getSlide().thumbEl;

                    if (!img) {
                        setFancyBoxBg(Fancybox, [0, 0, 0]);
                        return;
                    }

                    if (img.complete) {
                        sendImageToWorker(img);
                    } else {
                        img.addEventListener("load", () => {
                            sendImageToWorker(img);
                        });
                    }
                }
            },

            change: (carousel, index) => {
                if (
                    !(isLoading || isLastPage) &&
                    index >= carousel.getSlides().length - 5
                ) {
                    infiniteScroll.loadNextPage().then((loaded) => {
                        var items = loaded.items;
                        var slides = [];

                        items.forEach((item) => {
                            if (item.classList.contains("media-item"))
                                slides.push({
                                    src: item.dataset.src,
                                    thumb: item.querySelector("img")?.src,
                                    triggerEl: item,
                                    thumbEl: item.querySelector("img"),
                                });
                        });

                        carousel.add(slides);
                    });
                }
            },
        },
    },

    // mainClass: "fancybox-bg-class",
    mainStyle: {
        "--f-toolbar-padding": "8px",
        "--f-toolbar-gap": "8px",
        "--f-button-border-radius": "50%",
        "--f-thumb-width": "82px",
        "--f-thumb-height": "82px",
        "--f-thumb-opacity": "0.5",
        "--f-thumb-hover-opacity": "1",
        "--f-thumb-selected-opacity": "1",
        // "--fancybox-backdrop-bg": "#000",
    },
});

function setFancyBoxBg(rgb) {
    Fancybox.getInstance()
        .getContainer()
        .style.setProperty(
            "--fancybox-backdrop-bg",
            `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 0.5)`
        );
}

colorWorker.onmessage = (e) => {
    const color = e.data;

    if (color) {
        setFancyBoxBg(color);
    } else {
        setFancyBoxBg([0, 0, 0]);
    }
};

function sendImageToWorker(img) {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d", { willReadFrequently: true });

    const w = Math.min(img.naturalWidth, 100);
    const h = Math.min(img.naturalHeight, 100);

    canvas.width = w;
    canvas.height = h;

    ctx.drawImage(img, 0, 0, w, h);

    const imageData = ctx.getImageData(0, 0, w, h);
    colorWorker.postMessage(imageData);
}
