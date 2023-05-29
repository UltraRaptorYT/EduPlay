AFRAME.registerComponent("click-handler", {
  init: function () {
    const animatedMarker = document.querySelector("#animated-marker");
    const aEntity = document.querySelector("#animated-model");

    // every click, we make our model grow in size :)
    animatedMarker.addEventListener("click", function (ev, target) {
      console.log(ev.detail.intersection.point);
      // const scale = aEntity.getAttribute("scale");
      // Object.keys(scale).forEach((key) => (scale[key] = scale[key] + 1));
      // aEntity.setAttribute("scale", scale);
    });
  },
});
