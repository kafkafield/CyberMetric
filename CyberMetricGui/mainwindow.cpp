#include <cstdio>
#include <iostream>
#include <unistd.h>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "QImage"
#include "QLabel"
#include "QAction"
#include "QFileDialog"
#include "QFileInfo"

using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connect(ui->actionOpen_o, SIGNAL(triggered()), this, SLOT(open_file()));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{

    QLabel *imageLabel = new QLabel(this);
    string env = "cd ~/Documents/test \n source /etc/profile \n source ~/.bash_profile \n ";
    string mulutilpath = "$MULVALROOT/utils/";
    string cmd = "graph_gen.sh ~/Documents/test/input.P -v -p";
    string holeCmd = env + mulutilpath + cmd;
    system(holeCmd.c_str());
    QPixmap img1;
    img1.load("/Users/Saint/Documents/test/AttackGraph.png");
    imageLabel->setPixmap(img1);
    imageLabel->resize(img1.width(), img1.height());
    //cout << img1.width() <<endl<< img1.height() << endl;
    ui->scrollArea->setWidgetResizable(1);
    ui->scrollArea->setWidget(imageLabel);
}

void MainWindow::open_file()
{
    inputPath = QFileDialog::getOpenFileName(this,
        tr("Open Spreadsheet"), ".",
        tr("Spreadsheet files (*.P)"));
    //cout << inputPath.toStdString().c_str() << endl;
    QFileInfo fi = QFileInfo(inputPath);
    outDir = fi.absolutePath();
    cout << inputPath.toStdString().c_str() << endl;
    cout << outDir.toStdString().c_str() << endl;
}
