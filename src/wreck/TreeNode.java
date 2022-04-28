package wreck;

import java.util.ArrayList;

public class TreeNode {
    String value;
    ArrayList<TreeNode> children;

    public TreeNode(String value) {
        this.value = value;
        children = new ArrayList<>();
    }

    public void addChildren(TreeNode node) {
        children.add(node);
    }
}
