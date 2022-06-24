$(document).ready(function () {
    $(".increment-btn").click(function (e) {
        e.preventDefault();

        var inc_value = $(this)
            .closest(".product_data")
            .find(".qty-input")
            .val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value < 10) {
            value++;
            $(this).closest(".product_data").find(".qty-input").val(value);
        }
    });

    $(".decrement-btn").click(function (e) {
        e.preventDefault();

        var dcr_value = $(this)
            .closest(".product_data")
            .find(".qty-input")
            .val();
        var value = parseInt(dcr_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest(".product_data").find(".qty-input").val(value);
        }
    });

    $(".addToCartBtn").click(function (e) {
        e.preventDefault();

        var product_id = $(this)
            .closest(".product_data")
            .find(".prod_id")
            .val();
        var quantity = $(this)
            .closest(".product_data")
            .find(".qty-input")
            .val();
        var token = $("input[name= csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "/cart/add-to-cart",
            data: {
                product_id: product_id,
                quantity: quantity,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response);
                swal(response.status);
            },
        });
    });

    $(".changeQuantity").click(function (e) {
        e.preventDefault();

        var product_id = $(this)
            .closest(".product_data")
            .find(".prod_id")
            .val();
        var quantity = $(this)
            .closest(".product_data")
            .find(".qty-input")
            .val();
        var token = $("input[name= csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                product_id: product_id,
                quantity: quantity,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response);
            },
        });
    });

    $(document).on("click", ".delete-cart-item", function (e) {
        e.preventDefault();

        var product_id = $(this)
            .closest(".product_data")
            .find(".prod_id")
            .val();
        var token = $("input[name= csrfmiddlewaretoken]").val();

        $.ajax({
            method: "POST",
            url: "/delete-cart",

            data: {
                product_id: product_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response);
                swal(response.status);
            },
        });
        $(".cartdelete").load(location.href + " .cartdelete");
    });

    $(".addtowishlist").click(function (e) {
        e.preventDefault();

        var product_id = $(this)
            .closest(".product_data")
            .find(".prod_id")
            .val();
        var token = $("input[name= csrfmiddlewaretoken]").val();
        $.ajax({
            method: "POST",
            url: "/addtowishlist",
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response);
                swal(response.status);
            },
        });
    });

    $(document).on("click", ".delete-wishlist", function (e) {
        e.preventDefault();

        var product_id = $(this)
            .closest(".product_data")
            .find(".prod_id")
            .val();
        var token = $("input[name= csrfmiddlewaretoken]").val();

        $.ajax({
            method: "POST",
            url: "/delete-wishlist",
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response);
                swal(response.status);
            },
        });
        $("#wishlistdelete").load(location.href + " #wishlistdelete");
    });

    $(document).on("click", ".delete-adminprod", function (e) {
        e.preventDefault();

        var product_id = $(this)
            .closest(".product_data")
            .find(".prod_id")
            .val();
        var token = $("input[name= csrfmiddlewaretoken]").val();

        $.ajax({
            method: "POST",
            url: "/delete-adminprod",
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response);
                swal(response.status);
            },
        });
        $(".deleteadminprod").load(location.href + " .deleteadminprod");
    });
});
