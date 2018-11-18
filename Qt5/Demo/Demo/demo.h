#ifndef DEMO_H
#define DEMO_H

#include <QtWidgets/QMainWindow>
#include <QHeaderView>
#include <QComboBox>
#include "ui_demo.h"

class MyHorizontalHeader : public QHeaderView
{
	Q_OBJECT

public:
	MyHorizontalHeader(QWidget *parent = 0);
	virtual ~MyHorizontalHeader();

public Q_SLOTS:
	void handleSectionResized(int i, int oldSize, int newSize);
	void handleSectionMoved(int logical, int oldVisualIndex, int newVisualIndex);
	void handleComboboxSelect(int i);
protected:
	void scrollContentsBy(int dx, int dy);
	virtual void paintSection(QPainter *painter, const QRect &rect, int logicalIndex) const;
	void CreatHeaderObjects();
	void showEvent(QShowEvent *e);


private:
	QMap<int, QWidget*> headerWidgets;
	QVector<int>        vheaderPos;

};

class Demo : public QMainWindow
{
	Q_OBJECT

public:
	Demo(QWidget *parent = 0);
	~Demo();

private:
	Ui::DemoClass ui;
};

#endif // DEMO_H
