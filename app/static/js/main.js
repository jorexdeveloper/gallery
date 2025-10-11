// const preloader = document.querySelector("#preloader");
// if (preloader) {
//     window.addEventListener("load", () => {
//         setTimeout(() => {
//             preloader.classList.add("loaded");
//         }, 1000);
//         setTimeout(() => {
//             preloader.remove();
//         }, 2000);
//     });
// }

// var $wow = new WOW();
// $wow.init();

$(function () {
    var $pckry = $(".gallery-container").packery({
        itemSelector: ".gallery-item",
        columnWidth: ".gallery-item-sizer",
        gutter: ".gallery-gutter-sizer",
    });

    $pckry
        .imagesLoaded()
        .progress(function (instance, image) {
            $pckry.packery("layout");
            console.log("Loaded: ", image.img.src);
        })

        .done(function () {
            console.log("All images loaded.");
        })

        .fail(function () {
            console.log("An image or more failed to load.");
        })

        .always(function () {
            $pckry.packery("layout");
            // $pckry.find(".gallery-item").each(function (i, item) {
            //     var draggie = new Draggabilly(item);
            //     $pckry.packery("bindDraggabillyEvents", draggie);
            // });
            // console.log("Draggabilly events bound.");
        });

    $pckry.find("video").each(function (index, video) {
        $(video).on("loadedmetadata", function () {
            $pckry.packery("layout");
        });
    });
});

Fancybox.bind("[data-fancybox]", {
    idle: 2000,
    closeExisting: true,

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
                right: ["autoplay", "thumbs", "download", "close"],
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
