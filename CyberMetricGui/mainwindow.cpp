#include <cstdio>
#include <iostream>
#include <unistd.h>

#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "QImage"
#include "QLabel"

using namespace std;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    QLabel *imageLabel = new QLabel(this);
    system("cd ~/Documents/test \n source /etc/profile \n source ~/.bash_profile \n ~/Code/CyberMetric/mulval/utils/graph_gen.sh ~/Documents/test/input.P -v -p");
    //FILE * f = popen("~/Code/CyberMetric/mulval/utils/graph_gen.sh ~/Documents/test/input.P -v -p", "r");
    //pclose(f);
    QPixmap img1;
    img1.load("/Users/Saint/Documents/test/AttackGraph.png");
    imageLabel->setPixmap(img1);
    imageLabel->resize(img1.width(), img1.height());
    cout << img1.width() <<endl<< img1.height() << endl;
    ui->scrollArea->setWidgetResizable(1);
    ui->scrollArea->setWidget(imageLabel);
}
