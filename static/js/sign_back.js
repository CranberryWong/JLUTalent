function launchParticlesJS(e, i) {
    function a() {
        pJS.fn.canvasInit(),
        pJS.fn.canvasSize(),
        pJS.fn.canvasPaint(),
        pJS.fn.particlesCreate(),
        pJS.fn.particlesDraw()
    }
    function t() {
        pJS.fn.particlesDraw(),
        pJS.fn.requestAnimFrame = requestAnimFrame(t)
    }
    var n = document.querySelector("#" + e + " > canvas");
    if (pJS = {
        canvas: {
            el: n,
            w: n.offsetWidth,
            h: n.offsetHeight
        },
        particles: {
            color: "#fff",
            shape: "circle",
            opacity: 1,
            size: 2.5,
            size_random: !0,
            nb: 200,
            line_linked: {
                enable_auto: !0,
                distance: 100,
                color: "#fff",
                opacity: 1,
                width: 1,
                condensed_mode: {
                    enable: !0,
                    rotateX: 65e3,
                    rotateY: 65e3
                }
            },
            anim: {
                enable: !0,
                speed: 1
            },
            array: []
        },
        interactivity: {
            enable: !0,
            mouse: {
                distance: 100
            },
            detect_on: "canvas",
            mode: "grab",
            line_linked: {
                opacity: 1
            },
            events: {
                onclick: {
                    enable: !0,
                    mode: "push",
                    nb: 4
                }
            }
        },
        retina_detect: !1,
        fn: {
            vendors: {
                interactivity: {}
            }
        }
    },
    i) {
        if (i.particles) {
            var c = i.particles;
            if (c.color && (pJS.particles.color = c.color), c.shape && (pJS.particles.shape = c.shape), c.opacity && (pJS.particles.opacity = c.opacity), c.size && (pJS.particles.size = c.size), 0 == c.size_random && (pJS.particles.size_random = c.size_random), c.nb && (pJS.particles.nb = c.nb), c.line_linked) {
                var s = c.line_linked;
                if (0 == s.enable_auto && (pJS.particles.line_linked.enable_auto = s.enable_auto), s.distance && (pJS.particles.line_linked.distance = s.distance), s.color && (pJS.particles.line_linked.color = s.color), s.opacity && (pJS.particles.line_linked.opacity = s.opacity), s.width && (pJS.particles.line_linked.width = s.width), s.condensed_mode) {
                    var r = s.condensed_mode;
                    0 == r.enable && (pJS.particles.line_linked.condensed_mode.enable = r.enable),
                    r.rotateX && (pJS.particles.line_linked.condensed_mode.rotateX = r.rotateX),
                    r.rotateY && (pJS.particles.line_linked.condensed_mode.rotateY = r.rotateY)
                }
            }
            if (c.anim) {
                var p = c.anim;
                0 == p.enable && (pJS.particles.anim.enable = p.enable),
                p.speed && (pJS.particles.anim.speed = p.speed)
            }
        }
        if (i.interactivity) {
            var o = i.interactivity;
            if (0 == o.enable && (pJS.interactivity.enable = o.enable), o.mouse && o.mouse.distance && (pJS.interactivity.mouse.distance = o.mouse.distance), o.detect_on && (pJS.interactivity.detect_on = o.detect_on), o.mode && (pJS.interactivity.mode = o.mode), o.line_linked && o.line_linked.opacity && (pJS.interactivity.line_linked.opacity = o.line_linked.opacity), o.events) {
                var l = o.events;
                if (l.onclick) {
                    var S = l.onclick;
                    0 == S.enable && (pJS.interactivity.events.onclick.enable = !1),
                    "push" != S.mode && (pJS.interactivity.events.onclick.mode = S.mode),
                    S.nb && (pJS.interactivity.events.onclick.nb = S.nb)
                }
            }
        }
        pJS.retina_detect = i.retina_detect
    }
    pJS.particles.color_rgb = hexToRgb(pJS.particles.color),
    pJS.particles.line_linked.color_rgb_line = hexToRgb(pJS.particles.line_linked.color),
    pJS.retina_detect && window.devicePixelRatio > 1 && (pJS.retina = !0, pJS.canvas.w = 2 * pJS.canvas.el.offsetWidth, pJS.canvas.h = 2 * pJS.canvas.el.offsetHeight, pJS.particles.anim.speed = 2 * pJS.particles.anim.speed, pJS.particles.line_linked.distance = 2 * pJS.particles.line_linked.distance, pJS.particles.line_linked.width = 2 * pJS.particles.line_linked.width, pJS.interactivity.mouse.distance = 2 * pJS.interactivity.mouse.distance),
    pJS.fn.canvasInit = function() {
        pJS.canvas.ctx = pJS.canvas.el.getContext("2d")
    },
    pJS.fn.canvasSize = function() {
        pJS.canvas.el.width = pJS.canvas.w,
        pJS.canvas.el.height = pJS.canvas.h,
        window.onresize = function() {
            pJS && (pJS.canvas.w = pJS.canvas.el.offsetWidth, pJS.canvas.h = pJS.canvas.el.offsetHeight, pJS.retina && (pJS.canvas.w *= 2, pJS.canvas.h *= 2), pJS.canvas.el.width = pJS.canvas.w, pJS.canvas.el.height = pJS.canvas.h, pJS.fn.canvasPaint(), pJS.particles.anim.enable || (pJS.fn.particlesRemove(), pJS.fn.canvasRemove(), a()))
        }
    },
    pJS.fn.canvasPaint = function() {
        pJS.canvas.ctx.fillRect(0, 0, pJS.canvas.w, pJS.canvas.h)
    },
    pJS.fn.canvasRemove = function() {
        pJS.canvas.ctx.clearRect(0, 0, pJS.canvas.w, pJS.canvas.h)
    },
    pJS.fn.particle = function(e, i, a) {
        this.x = a ? a.x: Math.random() * pJS.canvas.w,
        this.y = a ? a.y: Math.random() * pJS.canvas.h,
        this.radius = (pJS.particles.size_random ? Math.random() : 1) * pJS.particles.size,
        pJS.retina && (this.radius *= 2),
        this.color = e,
        this.opacity = i,
        this.vx = -.5 + Math.random(),
        this.vy = -.5 + Math.random(),
        this.draw = function() {
            switch (pJS.canvas.ctx.fillStyle = "rgba(" + this.color.r + "," + this.color.g + "," + this.color.b + "," + this.opacity + ")", pJS.canvas.ctx.beginPath(), pJS.particles.shape) {
            case "circle":
                pJS.canvas.ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, !1);
                break;
            case "edge":
                pJS.canvas.ctx.rect(this.x, this.y, 2 * this.radius, 2 * this.radius);
                break;
            case "triangle":
                pJS.canvas.ctx.moveTo(this.x, this.y),
                pJS.canvas.ctx.lineTo(this.x + this.radius, this.y + 2 * this.radius),
                pJS.canvas.ctx.lineTo(this.x - this.radius, this.y + 2 * this.radius),
                pJS.canvas.ctx.closePath()
            }
            pJS.canvas.ctx.fill()
        }
    },
    pJS.fn.particlesCreate = function() {
        for (var e = 0; e < pJS.particles.nb; e++) pJS.particles.array.push(new pJS.fn.particle(pJS.particles.color_rgb, pJS.particles.opacity))
    },
    pJS.fn.particlesAnimate = function() {
        for (var e = 0; e < pJS.particles.array.length; e++) {
            var i = pJS.particles.array[e];
            i.x += i.vx * (pJS.particles.anim.speed / 2),
            i.y += i.vy * (pJS.particles.anim.speed / 2),
            i.x - i.radius > pJS.canvas.w ? i.x = i.radius: i.x + i.radius < 0 && (i.x = pJS.canvas.w + i.radius),
            i.y - i.radius > pJS.canvas.h ? i.y = i.radius: i.y + i.radius < 0 && (i.y = pJS.canvas.h + i.radius);
            for (var a = e + 1; a < pJS.particles.array.length; a++) {
                var t = pJS.particles.array[a];
                if (pJS.particles.line_linked.enable_auto && pJS.fn.vendors.distanceParticles(i, t), pJS.interactivity.enable) switch (pJS.interactivity.mode) {
                case "grab":
                    pJS.fn.vendors.interactivity.grabParticles(i, t)
                }
            }
        }
    },
    pJS.fn.particlesDraw = function() {
        pJS.canvas.ctx.clearRect(0, 0, pJS.canvas.w, pJS.canvas.h),
        pJS.fn.particlesAnimate();
        for (var e = 0; e < pJS.particles.array.length; e++) {
            var i = pJS.particles.array[e];
            i.draw("rgba(" + i.color.r + "," + i.color.g + "," + i.color.b + "," + i.opacity + ")")
        }
    },
    pJS.fn.particlesRemove = function() {
        pJS.particles.array = []
    },
    pJS.fn.vendors.distanceParticles = function(e, i) {
        var a = e.x - i.x,
        t = e.y - i.y,
        n = Math.sqrt(a * a + t * t);
        if (n <= pJS.particles.line_linked.distance) {
            var c = pJS.particles.line_linked.color_rgb_line;
            if (pJS.canvas.ctx.beginPath(), pJS.canvas.ctx.strokeStyle = "rgba(" + c.r + "," + c.g + "," + c.b + "," + (pJS.particles.line_linked.opacity - n / pJS.particles.line_linked.distance) + ")", pJS.canvas.ctx.moveTo(e.x, e.y), pJS.canvas.ctx.lineTo(i.x, i.y), pJS.canvas.ctx.lineWidth = pJS.particles.line_linked.width, pJS.canvas.ctx.stroke(), pJS.canvas.ctx.closePath(), pJS.particles.line_linked.condensed_mode.enable) {
                var a = e.x - i.x,
                t = e.y - i.y,
                s = a / (1e3 * pJS.particles.line_linked.condensed_mode.rotateX),
                r = t / (1e3 * pJS.particles.line_linked.condensed_mode.rotateY);
                i.vx += s,
                i.vy += r
            }
        }
    },
    pJS.fn.vendors.interactivity.listeners = function() {
        if ("window" == pJS.interactivity.detect_on) var e = window;
        else var e = pJS.canvas.el;
        if (e.onmousemove = function(i) {
            if (e == window) var a = i.clientX,
            t = i.clientY;
            else var a = i.offsetX,
            t = i.offsetY;
            pJS && (pJS.interactivity.mouse.pos_x = a, pJS.interactivity.mouse.pos_y = t, pJS.retina && (pJS.interactivity.mouse.pos_x *= 2, pJS.interactivity.mouse.pos_y *= 2), pJS.interactivity.status = "mousemove")
        },
        e.onmouseleave = function() {
            pJS && (pJS.interactivity.mouse.pos_x = 0, pJS.interactivity.mouse.pos_y = 0, pJS.interactivity.status = "mouseleave")
        },
        pJS.interactivity.events.onclick.enable) switch (pJS.interactivity.events.onclick.mode) {
        case "push":
            e.onclick = function() {
                if (pJS) for (var e = 0; e < pJS.interactivity.events.onclick.nb; e++) pJS.particles.array.push(new pJS.fn.particle(pJS.particles.color_rgb, pJS.particles.opacity, {
                    x: pJS.interactivity.mouse.pos_x,
                    y: pJS.interactivity.mouse.pos_y
                }))
            };
            break;
        case "remove":
            e.onclick = function() {
                pJS.particles.array.splice(0, pJS.interactivity.events.onclick.nb)
            }
        }
    },
    pJS.fn.vendors.interactivity.grabParticles = function(e, i) {
        var a = e.x - i.x,
        t = e.y - i.y,
        n = Math.sqrt(a * a + t * t),
        c = e.x - pJS.interactivity.mouse.pos_x,
        s = e.y - pJS.interactivity.mouse.pos_y,
        r = Math.sqrt(c * c + s * s);
        if (n <= pJS.particles.line_linked.distance && r <= pJS.interactivity.mouse.distance && "mousemove" == pJS.interactivity.status) {
            var p = pJS.particles.line_linked.color_rgb_line;
            pJS.canvas.ctx.beginPath(),
            pJS.canvas.ctx.strokeStyle = "rgba(" + p.r + "," + p.g + "," + p.b + "," + (pJS.interactivity.line_linked.opacity - r / pJS.interactivity.mouse.distance) + ")",
            pJS.canvas.ctx.moveTo(e.x, e.y),
            pJS.canvas.ctx.lineTo(pJS.interactivity.mouse.pos_x, pJS.interactivity.mouse.pos_y),
            pJS.canvas.ctx.lineWidth = pJS.particles.line_linked.width,
            pJS.canvas.ctx.stroke(),
            pJS.canvas.ctx.closePath()
        }
    },
    pJS.fn.vendors.destroy = function() {
        cancelAnimationFrame(pJS.fn.requestAnimFrame),
        n.remove(),
        delete pJS
    },
    a(),
    pJS.particles.anim.enable && t(),
    pJS.interactivity.enable && pJS.fn.vendors.interactivity.listeners()
}
function hexToRgb(e) {
    var i = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    e = e.replace(i,
    function(e, i, a, t) {
        return i + i + a + a + t + t
    });
    var a = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(e);
    return a ? {
        r: parseInt(a[1], 16),
        g: parseInt(a[2], 16),
        b: parseInt(a[3], 16)
    }: null
}
window.requestAnimFrame = function() {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
    function(e) {
        window.setTimeout(e, 1e3 / 60)
    }
} (),
window.cancelRequestAnimFrame = function() {
    return window.cancelAnimationFrame || window.webkitCancelRequestAnimationFrame || window.mozCancelRequestAnimationFrame || window.oCancelRequestAnimationFrame || window.msCancelRequestAnimationFrame || clearTimeout
} (),
window.particlesJS = function(e, i) {
    "string" != typeof e && (i = e, e = "particles-js"),
    e || (e = "particles-js");
    var a = document.createElement("canvas");
    a.style.width = "100%",
    a.style.height = "100%";
    var t = document.getElementById(e).appendChild(a);
    null != t && launchParticlesJS(e, i)
};