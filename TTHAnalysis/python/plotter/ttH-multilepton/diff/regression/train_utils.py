import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def plot_roc(true, pred, sample_weight=None, label='', plot=True, debug=False):
    fpr, tpr, thresholds = roc_curve(true, pred) if sample_weight is None else roc_curve(true, pred, sample_weight=sample_weight)
    roc_auc = auc(fpr, tpr)
    if roc_auc < 0.5:
        roc_auc = 1-roc_auc
        fpr=1-fpr
        tpr=1-tpr
    if debug:
        print('FPR range:', min(fpr),max(fpr))
        print('TPR range:', min(tpr),max(tpr))

    if plot:
        plt.figure()
        lw = 2
        plt.plot(fpr, tpr, color='darkorange',
                 lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curve for the %s dataset'%label)
        plt.legend(loc="lower right")
        plt.show()
    return roc_auc

def plot_rel_pred(true, pred, label):
    plt.hist2d(true,pred-true)
    plt.xlabel('True label')
    plt.ylabel('Pred label - true label (%s dataset)'%label)
    plt.show()
    
def plot_pred(true, pred, label):
    plt.hist2d(true,pred)
    plt.xlabel('True label')
    plt.ylabel('Pred label')
    plt.title('%s dataset'%label)
    plt.show()
    
def plot_weights(wgt, true, label):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.hist(wgt[true==1])
    ax1.set_title('Signal (%s dataset)'%label)
    ax1.set_yscale('log')

    ax2.hist(wgt[true==0])
    ax2.set_title('Background (%s dataset)'%label)
    ax2.set_yscale('log')

def plot_score(true, score, label):
    plt.hist(score[true==0], label='CP even')
    plt.hist(score[true==1], label='CP odd', )
    plt.title('Score (%s dataset)'%label)
    plt.legend(loc='best')
    plt.show()
    

def plot_scores(true_train, score_train, true_test, score_test):
    
    plt.hist(score_train[true_train==0], histtype="bar", label='CP even')
    plt.hist(score_train[true_train==1], histtype="bar", label='CP odd', )
    plt.hist(score_test[true_test==0], histtype="step", label='CP even')
    plt.hist(score_test[true_test==1], histtype="step", label='CP odd', )
    plt.title('Score')
    plt.legend(loc='best')
    plt.show()
