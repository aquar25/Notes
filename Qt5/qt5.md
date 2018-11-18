

### Qt5 自定义表头

实现自定义表头需要实现QHeaderView
在Qt官网的blog有给出方法：
1. 如果在构造时已经可以获取表头的列数和控件信息，可以在构造函数中把表头的每个列控件创建出来
2. 如果只有当显示时才知道列数，可以在`showEvent()`函数中再去创建控件
3. 如果表格大小会变化，需要响应`sectionResized`，根据每个section的宽度和位置重新显示
4. 如果表格支持列移动，需要响应`sectionMoved`，同样处理每个section的位置和大小2重新显示
由于作者没有给出完整代码，参考文章实现后，在放大或缩小后动态拉伸列的位置出现错位。
原因如下：
在QHeaderView基类的处理表头的每一个列section大小改变的实现中，判断了只要长度变化就会发出通知，而这个通知在每个section的长度重新计算之前发出的，因此在这个信号里面获取的每个section的位置还是上一次没有改变大小的位置，导致出错。

```c++
void QHeaderViewPrivate::resizeSections(QHeaderView::ResizeMode globalMode, bool useGlobalMode)
 for (int i = 0; i < sectionCount(); ++i) {
        if ((previousSectionResizeMode != newSectionResizeMode
                || previousSectionLength != newSectionLength) && i > 0) {
                // 当表格列宽或模式发生变化后才会更新每一个section的数据。例如平均拉伸时，由于多个列不能整除，因此前几个列为一个宽度，而后几个列为另一个宽度，此时只会在前几个列[start, end]一起更新宽度，同时存储在模型中的位置信息并没有重新计算，导致列的信息是错误的。
                int spanLength = (i - spanStartSection) * previousSectionLength;
                createSectionItems(spanStartSection, i - 1, spanLength, previousSectionResizeMode);
                //Q_ASSERT(headerLength() == length);
                spanStartSection = i;
        }
        // 每个列都会通知一次，但是相同列宽的数据item是一起更新的    
        if (newSectionLength != oldSectionLength)
                emit q->sectionResized(logicalIndex(i), oldSectionLength, newSectionLength);
    }
}

void QHeaderViewPrivate::createSectionItems(int start, int end, int size, QHeaderView::ResizeMode mode)
{
    // 一次更新一个区间范围的所有列宽
    int sizePerSection = size / (end - start + 1);
    if (end >= sectionItems.count()) {
        sectionItems.resize(end + 1);
        sectionStartposRecalc = true;
    }
    SectionItem *sectiondata = sectionItems.data();
    for (int i = start; i <= end; ++i) {
        length += (sizePerSection - sectiondata[i].size);
        // 标记是否重新计算位置
        sectionStartposRecalc |= (sectiondata[i].size != sizePerSection);
        sectiondata[i].size = sizePerSection;
        sectiondata[i].resizeMode = mode;
    }
}

```

解决方案：
1. 覆盖基类的`virtual void paintSection()`，每次绘制时，更新每个列控件的位置，此时都是已经算好位置信息的。缺点是只要有重绘，都会执行更新位置的方法。例如移动窗口或是有遮挡部分列头，都会触发这个事件处理。
`
2. 在子类中保存每个列的位置信息，自己计算每个列的开始位置，在`handleSectionResized`处理，只有当列宽变化时才会处理
```c++
void MyHorizontalHeader::handleSectionResized(int i, int oldSize, int newSize)
{
    // i的size变化后，i+1的位置需要更新
    int diff = newSize - oldSize;
    for (int col = i + 1; col < vheaderPos.size(); col++)
    {
        vheaderPos[col] += diff;
    }

    for (int j = visualIndex(i); j < count(); j++) {
        int logical = logicalIndex(j);
        if (headerWidgets[logical]!=nullptr)
        {
            headerWidgets[logical]->setGeometry(vheaderPos[logical], 0, newSize, height());
        }       
    }

    // not work well...
    //for (int j = visualIndex(i); j < count(); j++) {
    //  int logical = logicalIndex(j);
    //  if (headerWidgets[logical] != nullptr)
    //  {
    //      headerWidgets[logical]->setGeometry(sectionViewportPosition(logical), 0,
    //          sectionSize(logical) - 2, height());
    //  }
    //}
}
```

这个问题在baidu上几乎都是同一个解决方案，而用google才看到不同的实现。对于问题，有时需要静心调试，不能只是看别人那么写了，不一定适合自己的使用。使用一两个具体的例子在Qt的源码里面调试一下就可以找到问题的原因了，库没有错，别人的blog也没有错，只是具体问题需要具体分析，看多了也就习惯了。
