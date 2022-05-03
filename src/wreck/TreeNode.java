package wreck;

import java.util.ArrayList;

public class TreeNode {
    String value;
    ArrayList<TreeNode> children;

    public TreeNode(String value) {
        if (value.charAt(0) == 'x') {
            this.value = "" + (char)Integer.parseInt(value.substring(1, 3), 16);
        } else {
            this.value = value;
        }
        children = new ArrayList<>();
    }

    public void addChildren(TreeNode node) {
        children.add(node);
    }
}
