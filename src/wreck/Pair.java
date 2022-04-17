package wreck;

public class Pair<K, V> {
    private K key;
    private V value;

    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() {
        return key;
    }

    public V getValue() {
        return value;
    }

    public boolean equals(Pair<K, V> o) {
        return key.equals(o.key) && value.equals(o.value);
    }

    public String toString() {
        return "luther.Pair{" +
                "key=" + key +
                ", value=" + value +
                '}';
    }
}
