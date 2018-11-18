#include "demo.h"
#include <QLabel>
#include <QPainter>
#include <QObject>

Demo::Demo(QWidget *parent)
	: QMainWindow(parent)
{	
	ui.setupUi(this);
	MyHorizontalHeader* header = new MyHorizontalHeader(this);		
	ui.tableWidget->setHorizontalHeader(header);
	// 设置第一列固定宽度
	header->setSectionResizeMode(0, QHeaderView::Fixed);
	ui.tableWidget->setColumnWidth(0, 100);
	// 剩下列平均排满
	for (int i = 1; i < ui.tableWidget->columnCount(); i++)
	{
		header->setSectionResizeMode(i, QHeaderView::Stretch);
	}
}

Demo::~Demo()
{

}

MyHorizontalHeader::MyHorizontalHeader(QWidget *parent /*= 0*/) :QHeaderView(Qt::Horizontal, parent)
{
	connect(this, SIGNAL(sectionResized(int, int, int)), this,
		SLOT(handleSectionResized(int, int, int)));
	// 目前没有用到，可以不绑定
	connect(this, SIGNAL(sectionMoved(int, int, int)), this,
		SLOT(handleSectionMoved(int, int, int)));
	// 设置表头不可调整宽度
	//setSectionsMovable(true);

}

void MyHorizontalHeader::showEvent(QShowEvent *e)
{
	CreatHeaderObjects();
	QHeaderView::showEvent(e);

}

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
	//	int logical = logicalIndex(j);
	//	if (headerWidgets[logical] != nullptr)
	//	{
	//		headerWidgets[logical]->setGeometry(sectionViewportPosition(logical), 0,
	//			sectionSize(logical) - 2, height());
	//	}
	//}
}

void MyHorizontalHeader::handleSectionMoved(int logical, int oldVisualIndex, int newVisualIndex)
{
	for (int i = qMin(oldVisualIndex, newVisualIndex); i < count(); i++){
		int logical = logicalIndex(i);
		if (headerWidgets[logical])
		{
			headerWidgets[logical]->setGeometry(sectionViewportPosition(logical), 0,
				sectionSize(logical) - 2, height());
		}		
	}

}

void MyHorizontalHeader::scrollContentsBy(int dx, int dy)
{
	//QTableWidget::scrollContentsBy(dx, dy);
	//if (dx != 0)
	//	horizHeader->fixComboPositions();

}

void MyHorizontalHeader::CreatHeaderObjects()
{
	for (int i = 0; i < count(); i++) {
		if (i == 0 && headerWidgets[i]==nullptr)
		{
			QLabel* label = new QLabel(this);
			label->setText("yyyy");
			label->setGeometry(sectionViewportPosition(i), 0,
				sectionSize(i) - 2, height());
			headerWidgets[i] = label;
		}
		else
		{
			if (!headerWidgets[i]) 
			{
				QComboBox *box = new QComboBox(this);
				box->addItem("axxxxxxxxxxxxxxxxxx");
				box->addItem("bcccc");
				box->addItem("c");
				box->setObjectName(QString::number(i));
				headerWidgets[i] = box;
				QMetaObject::Connection con = connect(box, SIGNAL(currentIndexChanged(int)), this, SLOT(handleComboboxSelect(int)));
				Q_ASSERT(con);
			}
			headerWidgets[i]->setGeometry(sectionViewportPosition(i), 0,
				sectionSize(i) - 2, height());
		}
		vheaderPos.append(sectionViewportPosition(i));
		headerWidgets[i]->show();
	}
}

MyHorizontalHeader::~MyHorizontalHeader()
{

}

// an easy way to handle the position
void MyHorizontalHeader::paintSection(QPainter *painter, const QRect &rect, int logicalIndex) const
{
	painter->save();
	QHeaderView::paintSection(painter, rect, logicalIndex);
	painter->restore();

	if (headerWidgets[logicalIndex] != nullptr)
	{
		headerWidgets[logicalIndex]->setGeometry(sectionViewportPosition(logicalIndex), 0,
			sectionSize(logicalIndex) - 2, height());
	}
}

void MyHorizontalHeader::handleComboboxSelect(int i)
{
	QComboBox* pCombobox = dynamic_cast<QComboBox*>(sender());
	if (pCombobox!=nullptr)
	{
		QString name = pCombobox->objectName();
		int id = name.toInt();

	}
}


