import numpy as np

def compute_score(logits, labels, cutoff, normalize):
    predictions = np.argsort(-logits, axis=1)[:,:cutoff]
    batch_size, _ = labels.shape
    scores = []
    for batch in range(batch_size):
        label_bt = labels[batch,:]
        label_bt = np.nonzero(label_bt)[0]
        prediction_bt = predictions[batch,:]
        num_label = len(label_bt)
        present = 0
        for label in label_bt:
            if label in prediction_bt:
                present += 1
        score = present
        if score > 0:
            score *= (1.0 / normalize(cutoff, num_label))
        # print('score={0:.4f}'.format(score))
        scores.append(score)
    score = np.mean(scores)
    return score

def compute_hit(logits, labels, cutoff):
    def normalize(cutoff, num_label):
        return min(cutoff, num_label)
    hit = compute_score(logits, labels, cutoff, normalize)
    # print('hit={0:.4f}'.format(hit))
    return hit

def compute_rec(logits, labels, cutoff):
    def normalize(cutoff, num_label):
        return num_label
    rec = compute_score(logits, labels, cutoff, normalize)
    # print('rec={0:.4f}'.format(rec))
    return rec

def compute_acc(predictions, labels):
    acc = np.average(predictions == labels)
    return acc

def eval_mdlcompr(sess, vd_model, mnist):
  vd_image_np, vd_label_np = mnist.test.images, mnist.test.labels
  feed_dict = {vd_model.image_ph:vd_image_np}
  predictions, = sess.run([vd_model.predictions], feed_dict=feed_dict)
  acc_v = compute_acc(predictions, vd_label_np)
  return acc_v

def main():
    logits = np.log([
        [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4],
        [0.1, 0.2, 0.3, 0.4], [0.1, 0.2, 0.3, 0.4],
    ])
    labels = np.asarray([
        [0, 0, 0, 0], [0, 0, 0, 1],
        [0, 0, 1, 1], [1, 1, 1, 0],
    ], dtype=np.int32)
    cutoff = 2

    # hit = compute_hit(logits, labels, cutoff)
    # print('hit=%.4f' % (hit))

    # rec = compute_rec(logits, labels, cutoff)
    # print('rec=%.4f' % (rec))

    predictions = np.asarray([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    labels = np.asarray([0, 1, 3, 3, 4, 5, 6, 8, 8, 9])
    acc = compute_acc(predictions, labels)
    print('acc=%.4f' % (acc))

if __name__ == '__main__':
    main()