import UIKit

final class SampleViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
    }

    @objc func exposedToObjC() {
        print("objc")
    }
}

struct SampleModel {
    var title: String = ""
}

extension SampleViewController {
    func helperMethod() {
        print("help")
    }
}
