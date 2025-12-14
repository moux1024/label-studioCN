const { I } = inject();

module.exports = {
  seeWarning(text) {
    I.seeElement(".ant-modal");
    I.see("警告");
    I.see(text);
    I.waitTicks(3);
    I.see("确定");
  },
  dontSeeWarning(text) {
    I.dontSeeElement(".ant-modal");
    I.dontSee("警告");
    I.dontSee(text);
  },
  closeWarning() {
    I.click("确定");
    I.waitToHide(".ant-modal");
  },
};
