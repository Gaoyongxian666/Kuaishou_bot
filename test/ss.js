define("web:component/reflow_video/index", function (a, t, e) {
    e.exports = Pagelet.extend(
        {
            el: "#pageletReflowVideo", events: {"click $player": "onPlayVideo"}, channels: {}, init: function (a) {
                this.data = a, this.render()
            }, hasDataRender: function (a) {
                try {
                    $(".detail.clrfix").removeClass("not-found"), $(".bg-ground-anchor").attr("style", "background-image:url(".concat(a.video.cover.url_list[0], ")")), $(".user-avator-anchor").attr("src", a.author.avatar_thumb.url_list[0]), $(".name.nowrap").text("@" + a.author.nickname), a.cha_list & & a.cha_list[0] ? $(".challenge-info .inner").text(a.cha_list[0].cha_name) : $
                    (".challenge-info").attr("style", "display: none"), $(".desc").text(a.desc)
                } catch (t) {
                    this.hasNoDataRender()
                }
            }, hasNoDataRender: function () {
                $(".detail.clrfix").addClass("not-found"), $(".bg-ground-anchor").attr("style", "background-image:url()"), $(
                    ".user-avator-anchor").attr(
                    "src", ""), $(".name.nowrap").text(""), $(".challenge-info").attr("style", "display: none"), $(".desc").attr("style",
                    "display: none")
            },
            render: function () {
                var a = this;
                this.data.itemId || (this.data.itemId = location.pathname.replace(/ ^ \ / |;\ / $ /g, "").split("/")[2]),


                $.get(
                    "/web/api/v2/aweme/iteminfo/", {item_ids: this.data.itemId, dytk: this.data.dytk}, function (t) {
                        if (0 === t.status_code) {
                            var
                                e = t.item_list[0], i = !!e;
                            if (!i)
                                return void
                                    a.hasNoDataRender();
                            a.hasDataRender(e);
                            try {
                                a.data.videoWidth = e.video.width | | 750, a.data.videoHeight = e.video.height | | 1334, a.data.playAddr =
                                    e.video.play_addr.url_list[0], a.data.cover = e.video.cover.url_list[0], a.data.hasData = i
                            } catch (d) {
                                return void
                                    a.hasNoDataRender()
                            }
                            var
                                o = a.$dom.player, r = a.data.videoWidth, n = a.data.videoHeight, s = o.width(),
                                l = s * n / r;
                            o.css("height", l)
                        }
                    })
            }, onPlayVideo: function () {
                var
                    a = this.$dom.player;
                if (!this.loaded) {
                    this.loaded = !0;
                    var
                        t = this.data.hasData;
                    if (!t)
                        return;
                    var
                        e = $("<video>",
                            {
                                "class": "player",
                                src: this.data.playAddr,
                                poster: this.data.cover,
                                type: "video/mp4",
                                preload: "auto",
                                controls: "true",
                                width: "100%"
                            });
                    a.append(e), this.orgPlayer = e[0], this.orgPlayer.play(), e.on("play", function () {
                        a.addClass("playing")
                    }).on("pause", function () {
                        a.removeClass("playing")
                    })
                }
            }
        })
});
