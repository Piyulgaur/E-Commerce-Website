document
.getElementsByTagName("push-to-talk-button")[0]
.addEventListener("speechsegment", (e) => {
    e.detail.entities.forEach((entity) => {
      document.getElementById(entity.type).value = entity.value;
    });
  });
