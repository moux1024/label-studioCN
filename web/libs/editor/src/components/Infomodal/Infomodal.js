import { Modal } from "antd";

const wrapper = (_type, value, title) => {
  const custom = {
    type: "",
    title: "",
  };

  switch (_type) {
    case "error":
      custom.type = Modal.error;
      custom.title = "错误";
      break;
    case "warning":
      custom.type = Modal.warning;
      custom.title = "警告";
      break;
    case "success":
      custom.type = Modal.success;
      custom.title = "成功";
      break;
    default:
      custom.type = Modal.info;
      custom.title = "信息";
  }

  return custom.type({
    title: title ? title : custom.title,
    content: value,
  });
};

/**
 * Success modal
 * @param {string} value
 * @param {string} title
 */
const error = (value, title) => {
  return wrapper("error", value, title);
};

/**
 * Warning modal
 * @param {string} value
 * @param {string} title
 */
const warning = (value, title) => {
  return wrapper("warning", value, title);
};

/**
 * Success modal
 * @param {string} value
 * @param {string} title
 */
const success = (value, title) => {
  return wrapper("success", value, title);
};

/**
 * Information modal
 * @param {string} value
 * @param {string} title
 */
const info = (value, title) => {
  return wrapper("info", value, title);
};

export default { error, warning, success, info };
