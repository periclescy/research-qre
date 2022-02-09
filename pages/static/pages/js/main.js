let cropper1;
let cropper2;
let canvas1;
let canvas2;
let data1;
let data2;

$(document).ready(function () {

    /*** Get Next button timestamp ***/
    $('#next-form').submit(function () {
        document.getElementById('id_next_t').value = Date.now(); //timestamp in EpochTime (milliseconds UTC)
    });

    /*** ********************* ***/


    /*** Get CSRF from cookies ***/

    let dict = document.cookie.split(':').map(cookie => cookie.split('=')).reduce((accumulator, [key, value]) => ({...accumulator, [key.trim()]: decodeURIComponent(value)}), {});
    let csrf_variable = dict["csrftoken"];

     /*** *************************** ***/

    /*** Cropper js General settings ***/
    Cropper.setDefaults({
        viewMode: 1
    })
    /*** *************************** ***/

    /*** Create hidden Target boxes and load Cropper boxes ***/

    // Set variables for pictures
    let image_pri = document.getElementById('img_pri');
    let image_sec = document.getElementById('img_sec');

    // Create cropper for primary picture
    cropper1 = new Cropper(image_pri, {
        ready: function() {
            canvas1 = this.cropper.getCanvasData();
            console.log("Canvas1 before Ajax", canvas1);
        }
    });

    // If Secondary picture has target
    if (spot_sec != null) {

        // Create cropper for secondary picture
        cropper2 = new Cropper(image_sec, {
            ready: function() {
                canvas2 = this.cropper.getCanvasData();
                console.log("Canvas2 before Ajax", canvas2);
            }
        });

        $("#confirm_button").on('click', function () {

            let t = Date.now(); //timestamp in EpochTime (milliseconds UTC)

            data1 = cropper1.getData();
            data2 = cropper2.getData();
            console.log(data1, data2);

            stop_Countdown();

            // AJAX POST
            $.ajax({
                type: "POST",
                url: "/home",
                dataType: "json",
                async: true,
                data: {
                    t:t,
                    x_p: data1['x'],
                    y_p: data1['y'],
                    w_p: data1['width'],
                    h_p: data1['height'],
                    x_s: data2['x'],
                    y_s: data2['y'],
                    w_s: data2['width'],
                    h_s: data2['height'],
                    Post_name: "commit-target",
                    csrfmiddlewaretoken: csrf_variable
                },
                success: function (obj) {
                    let s = obj.total_score;
                    let elem = document.getElementById('total-score');
                    let elem_box = document.getElementById('alert-score');
                    // elem.innerHTML = s + '%';
                    elem_box.classList.remove("d-none");
                    if (s < 70) {
                        elem_box.classList.add("alert-warning");
                        elem.innerHTML = 'Καλή προσπάθεια';
                    }
                    else if (s >= 70) {
                        elem_box.classList.add("alert-success");
                        elem.innerHTML = 'Excellent!';
                    }

                    console.log("Right after success", obj);

                    // Create hidden target box for primary picture
                    $('<div class="target_selected" style="left:' + obj.xtl_pri + '%; top:'
                        + obj.ytl_pri + '%; width: ' + obj.w_pri + '%; height: ' + obj.h_pri
                        + '%;"></div>.').appendTo(".image-box-pri");
                        // Create hidden target box for secondary picture
                    $('<div class="target_selected" style="left:' + obj.xtl_sec + '%; top:'
                        + obj.ytl_sec + '%; width: ' + obj.w_sec + '%; height: ' + obj.h_sec
                        + '%;"></div>.').appendTo(".image-box-sec");
                }

                })
            }); // End of AJAX

        // Create hidden target box for primary picture
        $('<div class="target d-none" style="left:' + spot_pri[0] + '%; top:'
            + spot_pri[1] + '%; width: ' + spot_pri[2] + '%; height: ' + spot_pri[3]
            + '%;"></div>.').appendTo(".image-box-pri");
        // Create hidden target box for secondary picture
        $('<div class="target d-none" style="left:' + spot_sec[0] + '%; top:'
            + spot_sec[1] + '%; width: ' + spot_sec[2] + '%; height: ' + spot_sec[3]
            + '%;"></div>.').appendTo(".image-box-sec");
    }
    else {
        $("#confirm_button").on('click', function () {

            let t = Date.now(); //timestamp in EpochTime (milliseconds UTC)

            data1 = cropper1.getData();
            console.log(data1);

            stop_Countdown();

            // AJAX POST
            $.ajax({
                type: "POST",
                url: "/home",
                dataType: "json",
                async: true,
                data: {
                    t:t,
                    x_p: data1['x'],
                    y_p: data1['y'],
                    w_p: data1['width'],
                    h_p: data1['height'],
                    Post_name: "commit-target",
                    csrfmiddlewaretoken: csrf_variable
                },
                success: function (obj) {
                    console.log(obj);
                    let s = obj.total_score;
                    let elem = document.getElementById('total-score');
                    let elem_box = document.getElementById('alert-score');
                    elem_box.classList.remove("d-none");
                    if (s < 70) {
                        elem_box.classList.add("alert-warning");
                        elem.innerHTML = 'Nice try.';
                    }
                    else if (s >= 70) {
                        elem_box.classList.add("alert-success");
                        elem.innerHTML = 'Excellent!';
                    }

                    console.log("Right after success", obj);

                    // Create hidden target box for primary picture
                    $('<div class="target_selected" style="left:' + obj.xtl_pri + '%; top:'
                        + obj.ytl_pri + '%; width: ' + obj.w_pri + '%; height: ' + obj.h_pri
                        + '%;"></div>.').appendTo(".image-box-pri");

                }
            }); // End of AJAX
        })
        // Create hidden target box for primary picture
        $('<div class="target d-none" style="left:' + spot_pri[0] + '%; top:'
            + spot_pri[1] + '%; width: ' + spot_pri[2] + '%; height: ' + spot_pri[3]
            + '%;"></div>.').appendTo(".image-box-pri");

        // Show box since secondary picture has no targets
        $('#img_sec').css('border', '4px solid rgba(0, 255, 0, 1)');
    }

    /*** *********************************************************** ***/

    /*** Targets CountDown timer ***/

    let time_left;
    time_left = countdown_per_pic * 1000;

    // Calculate total countdown time
    let countDown_total = Date.now() + time_left;

    // Create countdown timer
    let x = setInterval(run_Countdown, 1000)

    function run_Countdown () {
        // Find the distance between now and the count down total
        let distance = countDown_total - Date.now();
        let countdown = Math.round(distance / 1000);

        // Output the result in an element
       $('#countdown').html(countdown + " sec ");

        // Color change when countdown is approaching zero
        if (countdown < 10 && countdown >= 4) {
            $('#countdown').css({"color": "yellow"});
        }
        else if (countdown < 4 && countdown > 0) {
            $('#countdown').css({"color": "red"});
        }
        // When countdown is over
        else if (countdown <= 0) {

            clearInterval(x);
            $('.image-fit').off('click'); //Disable click functionality for missed clicks
            $('img').css('filter', 'drop-shadow(10px 10px 10px gray)'); // Make effects
            $('#countdown').html("EXPIRED");
            $("#next_button").removeClass("pointer_none d-none");
            $("#confirm_button").addClass("pointer_none d-none");
            $(".description-progress").removeClass("d-none");

            // Disable Cropper for pictures
            image_pri.cropper.destroy();
            if (spot_sec != null) {
                image_sec.cropper.destroy();
            }
            //Reveal missed targets after clock is Expired
            $(".target").removeClass("d-none").addClass("target_expired pointer_none");


            // AJAX POST
            $.ajax({
                type: "POST",
                url: "/home",
                dataType: "json",
                async: true,
                data: {
                    t:countDown_total,
                    Post_name: "expired-target",
                    csrfmiddlewaretoken: csrf_variable
                },
                success: function () {
                    console.log('Expired!');
                }
            }); // End of AJAX


        }
    }
    function stop_Countdown() {
        clearInterval(x);
        $("#next_button").removeClass("pointer_none d-none");
        $("#confirm_button").addClass("pointer_none d-none");
        $(".description-progress").removeClass("d-none");

        //Reveal missed targets
        $(".target").removeClass("d-none").addClass("target_expired pointer_none");

        // Disable Cropper for pictures
        cropper1.setCanvasData(canvas1);
        cropper1.setData(data1);
        image_pri.cropper.disable();
        if (spot_sec != null) {
            cropper2.setCanvasData(canvas2);
            cropper2.setData(data2);
            image_sec.cropper.disable();

        }
    }

})