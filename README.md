# KOR_president-election-cosine-distance

From the presidential election debate on May 2025, two interesting points were found which show difference between dialogue of debate and actual comments(especially best 50 liked comments).
This code helps us to understand the cosine distance between debate dialogue and comments.


<img width="602" height="332" alt="사진 3" src="https://github.com/user-attachments/assets/90acea3b-9f7b-429d-ba37-964a515c1437" />



This graph is the output of the code, and it describes that there was some actual distance between debate dialogue and comments.
두 영상에서, 전체 댓글과 토론 전문 사이의 코사인 유사도, 자주 노출되는 상위 50개 댓글과 토론 전문 사이의 코사인 유사도를 측정한 결과는 위 그래프와 같다. 흥미로운 것은 두 영상 모두에서 상위 50개 댓글과 토론 전문 사이의 거리가 전체 댓글과 토론 전문 사이의 거리보다 크게 측정되었는데. 이를 통해 두 가지를 추론할 수 있다. 첫째, 자주 노출되는 댓글에 의해 인지부조화는 재생산된다고 볼 여지가 있다. 둘째, 추천을 많이 받은 댓글은 의도적으로 인지부조화를 유도하기 위한 정치 고관여층에 의해 작성된다고 볼 여지가 있다.

따라서 댓글창에서의 논쟁은 토론에서의 논쟁과 그 내용 면에서 상당한 괴리가 있으며, 이는 토론 영상에서 언급되고 있는 사실에 대한 논의를 피하는 인지부조화로부터 기인했다고 볼 수 있다. 이는 토론 영상이 시사하고 있는 사회정치적 사실에 대한 논의보다는 상대 진영 후보를 깎아내리면서 자신이 지지하는 후보의 논리를 정당화하기 위한 캔슬 컬처가 댓글창에서 벌어졌다고 해석할 수 있다. 즉, 객관적 토론 맥락을 그대로 받아들이는 것이 자신들이 가지고 있던 신념과 불일치할 때, 이 불일치에서 오는 불편함을 실제 정보를 왜곡하거나 선입견에 부합하는 방향의 댓글을 작성하는 방식으로 해소하려 한다는 것이다.

이러한 인지적 왜곡을 기반으로 쓰여진 댓글은 내가 지지하는 정치인의 주장을 더욱 공고화하고, 다른 정치인의 논리적 정합성을 약화시키려는 온라인 공론장 캔슬 컬처로 작동한다 볼 수 있다. 또한 존재하는 사실을 존재하지 않는 것으로 간주함으로써, 공론장의 다양성을 뭉개버린다. 이런 인지부조화에 의한 캔슬 컬처는 캔슬을 시도한 사람의 논리적 정합성을 담보하지도 않고, 감정적 표현에 기댄 조롱과 비생산적 논의로 이어짐으로써 공론장의 황폐화를 가속한다는 점에서 문제가 된다.

다만 이러한 코사인 유사도 분석만으로 '인지부조화'라는 심리학적 개념을 단정하기에는 한계가 있다. 유사도 차이가 발생하는 원인은 인지부조화 외에도 다양할 수 있기 때문이다. 따라서 본 분석은 댓글과 토론 내용 사이의 '괴리'를 수치적으로 확인한 것에 의의가 있으며, 이러한 괴리 현상이 온라인 공론장에서 어떤 의미를 갖는지에 대한 해석은 보다 신중할 필요가 있다. 그럼에도 불구하고 이런 괴리 자체가 공론장의 건전성에 미치는 영향은 여전히 주목할 만한 지점이라고 할 수 있다.
