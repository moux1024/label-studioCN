export const simpleTextConfig = `<View>
    <Text name="text" value="$text" />
    <Labels name="label" toName="text">
      <Label value="标签" />
    </Labels>
  </View>`;

export const simpleTextData = {
  text: "Hello world!",
};

export const simpleTextResult = [
  {
    id: "1",
    from_name: "label",
    to_name: "text",
    type: "labels",
    value: {
      start: 6,
      end: 11,
      text: "world",
      labels: ["标签"],
    },
  },
  {
    id: "2",
    from_name: "label",
    to_name: "text",
    type: "labels",
    value: {
      start: 0,
      end: 5,
      text: "Hello",
      labels: ["标签"],
    },
  },
];
